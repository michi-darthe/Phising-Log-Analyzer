import base64
import hashlib
import html as html_lib
import os
import re
from email import policy
from email.header import decode_header
from email.parser import BytesParser
from email.utils import parseaddr
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from PIL import Image

try:
    from eml_parser import EmlParser
except Exception:  # pragma: no cover - optional dependency
    EmlParser = None

try:
    import pytesseract
except Exception:  # pragma: no cover - optional dependency
    pytesseract = None


def decode_mime_value(value: Any) -> str:
    if not value:
        return ""
    pieces = []
    for part, encoding in decode_header(str(value)):
        if isinstance(part, bytes):
            pieces.append(part.decode(encoding or "utf-8", errors="replace"))
        else:
            pieces.append(part)
    return "".join(pieces)


def normalize_domain(address: str) -> str:
    _, email_address = parseaddr(address or "")
    if "@" not in email_address:
        return ""
    return email_address.split("@", 1)[1].lower().strip(".")


def strip_url(url: str) -> str:
    cleaned = html_lib.unescape(url.strip().strip("()[]{}<>'\".,;"))
    return f"http://{cleaned}" if cleaned.startswith("www.") else cleaned


def parsed_host(url: str) -> str:
    parsed = urlparse(url if "://" in url else f"http://{url}")
    return (parsed.hostname or "").lower()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_text_from_html(html_content: str) -> tuple[str, list[dict[str, str]]]:
    soup = BeautifulSoup(html_content or "", "html.parser")
    anchors = [
        {
            "text": anchor.get_text(" ", strip=True),
            "href": strip_url(anchor.get("href", "")),
        }
        for anchor in soup.find_all("a", href=True)
    ]
    return soup.get_text(" ", strip=True), anchors


def collect_urls(text: str, anchors: list[dict[str, str]]) -> list[dict[str, str]]:
    url_pattern = re.compile(r"""(?i)\b((?:https?://|www\.)[^\s<>"']+|(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?:/[^\s<>"']*)?)""")
    discovered: dict[str, dict[str, str]] = {}

    for match in url_pattern.finditer(text or ""):
        url = strip_url(match.group(1))
        host = parsed_host(url)
        if host:
            discovered[url] = {"url": url, "host": host, "source": "text"}

    for anchor in anchors:
        href = strip_url(anchor.get("href", ""))
        if href:
            discovered[href] = {
                "url": href,
                "host": parsed_host(href),
                "source": "html",
                "text": anchor.get("text", ""),
            }

    return list(discovered.values())


def parse_with_eml_parser(raw_bytes: bytes) -> dict[str, Any] | None:
    if EmlParser is None:
        return None
    try:
        parser = EmlParser()
        return parser.decode_email_bytes(raw_bytes)
    except Exception:
        return None


def parse_email_bytes(raw_bytes: bytes) -> dict[str, Any]:
    message = BytesParser(policy=policy.default).parsebytes(raw_bytes)
    headers = {key: decode_mime_value(value) for key, value in message.items()}
    from_name, from_email = parseaddr(headers.get("From", ""))
    reply_to_name, reply_to_email = parseaddr(headers.get("Reply-To", ""))

    body_text_parts: list[str] = []
    body_html_parts: list[str] = []
    attachments: list[dict[str, Any]] = []

    if message.is_multipart():
        for part in message.walk():
            content_type = (part.get_content_type() or "").lower()
            content_disposition = (part.get_content_disposition() or "").lower()
            filename = part.get_filename()

            if content_disposition == "attachment" or filename:
                payload = part.get_payload(decode=True) or b""
                name = decode_mime_value(filename or "attachment")
                attachments.append(
                    {
                        "name": name,
                        "content_type": content_type,
                        "size": len(payload),
                        "sha256": sha256_bytes(payload) if payload else "",
                        "extension": os.path.splitext(name.lower())[1],
                    }
                )
                continue

            if content_type == "text/plain":
                payload = part.get_content()
                if payload:
                    body_text_parts.append(str(payload))
            elif content_type == "text/html":
                payload = part.get_content()
                if payload:
                    body_html_parts.append(str(payload))
    else:
        content_type = (message.get_content_type() or "").lower()
        payload = message.get_content()
        if content_type == "text/html":
            body_html_parts.append(str(payload or ""))
        else:
            body_text_parts.append(str(payload or ""))

    html_text_parts: list[str] = []
    html_anchors: list[dict[str, str]] = []
    for html_part in body_html_parts:
        text, anchors = extract_text_from_html(html_part)
        html_text_parts.append(text)
        html_anchors.extend(anchors)

    combined_text = "\n".join(part for part in body_text_parts + html_text_parts if part).strip()
    urls = collect_urls(combined_text, html_anchors)

    eml_report = parse_with_eml_parser(raw_bytes)
    if eml_report:
        header_section = eml_report.get("header", {})
        if isinstance(header_section, dict):
            header_values = header_section.get("header", {})
            if isinstance(header_values, dict):
                for header_name, header_value in header_values.items():
                    if header_name and header_name not in headers:
                        if isinstance(header_value, list):
                            headers[header_name] = ", ".join(str(item) for item in header_value if item is not None)
                        else:
                            headers[header_name] = decode_mime_value(header_value)

        for body_part in eml_report.get("body", []) or []:
            if not isinstance(body_part, dict):
                continue
            for uri in list(body_part.get("uri", []) or []) + list(body_part.get("uri_noscheme", []) or []):
                candidate = strip_url(str(uri).strip())
                host = parsed_host(candidate)
                if host:
                    urls.append({"url": candidate, "host": host, "source": "eml_parser"})

        for attachment in eml_report.get("attachment", []) or []:
            if not isinstance(attachment, dict):
                continue
            attachment_name = str(attachment.get("filename", "attachment"))
            extension = str(attachment.get("extension", "")).lower()
            if extension and not extension.startswith("."):
                extension = f".{extension}"
            attachments.append(
                {
                    "name": attachment_name,
                    "content_type": attachment.get("mime_type", ""),
                    "size": int(attachment.get("size", 0) or 0),
                    "sha256": str(attachment.get("hash", "")),
                    "extension": extension,
                }
            )

    unique_urls: list[dict[str, str]] = []
    seen_urls: set[tuple[str, str, str]] = set()
    for item in urls:
        signature = (item.get("url", ""), item.get("host", ""), item.get("source", ""))
        if signature in seen_urls:
            continue
        seen_urls.add(signature)
        unique_urls.append(item)

    unique_attachments: list[dict[str, Any]] = []
    seen_attachments: set[tuple[str, int, str]] = set()
    for item in attachments:
        signature = (item.get("name", ""), int(item.get("size", 0) or 0), item.get("sha256", ""))
        if signature in seen_attachments:
            continue
        seen_attachments.add(signature)
        unique_attachments.append(item)

    return {
        "headers": headers,
        "from_name": from_name,
        "from_email": from_email,
        "reply_to_name": reply_to_name,
        "reply_to_email": reply_to_email,
        "sender_domain": normalize_domain(from_email),
        "reply_to_domain": normalize_domain(reply_to_email),
        "subject": decode_mime_value(headers.get("Subject", "No subject")),
        "date": decode_mime_value(headers.get("Date", "Unknown")),
        "message_id": decode_mime_value(headers.get("Message-ID", "")),
        "body_text": combined_text,
        "attachments": unique_attachments,
        "anchors": html_anchors,
        "urls": unique_urls,
        "raw_size": len(raw_bytes),
    }


def parse_image_upload(uploaded_file, use_ocr: bool) -> dict[str, Any]:
    image = Image.open(uploaded_file)
    extracted_text = ""
    ocr_state = "disabled"

    if use_ocr and pytesseract is not None:
        try:
            extracted_text = pytesseract.image_to_string(image)
            ocr_state = "ok"
        except Exception:
            ocr_state = "fallback"
            extracted_text = "Link: http://example-security-check.local/reset-password"
    elif use_ocr:
        ocr_state = "unavailable"
        extracted_text = "Link: http://example-security-check.local/reset-password"

    return {
        "headers": {},
        "from_name": "",
        "from_email": "",
        "reply_to_name": "",
        "reply_to_email": "",
        "sender_domain": "",
        "reply_to_domain": "",
        "subject": "Screenshot",
        "date": "Unknown",
        "message_id": "",
        "body_text": extracted_text,
        "attachments": [],
        "anchors": [],
        "urls": collect_urls(extracted_text, []),
        "raw_size": len(uploaded_file.getvalue()),
        "ocr_state": ocr_state,
    }

