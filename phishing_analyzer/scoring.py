import ipaddress
from dataclasses import dataclass, asdict
from typing import Any

from .config import ARCHIVE_EXTENSIONS, MACRO_EXTENSIONS, SUSPICIOUS_EXTENSIONS, SUSPICIOUS_KEYWORDS, URL_SHORTENERS
from .parsing import parsed_host


@dataclass
class Signal:
    title: str
    detail: str
    points: int
    severity: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def host_is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def looks_suspicious_tld(host: str) -> bool:
    return any(host.endswith(tld) for tld in {".zip", ".mov", ".top", ".xyz", ".click", ".icu", ".ru", ".cn"})


def domain_matches(base_domain: str, candidate_host: str) -> bool:
    if not base_domain or not candidate_host:
        return True
    return candidate_host == base_domain or candidate_host.endswith(f".{base_domain}") or base_domain.endswith(f".{candidate_host}")


def extract_visible_host(text: str) -> str:
    return parsed_host(text)


def score_report(report: dict[str, Any]) -> dict[str, Any]:
    score = 0
    signals: list[Signal] = []
    categories = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    def add_signal(title: str, detail: str, points: int, severity: str) -> None:
        nonlocal score
        score += points
        categories[severity] += 1
        signals.append(Signal(title=title, detail=detail, points=points, severity=severity))

    headers = report.get("headers", {})
    body_text = (report.get("body_text") or "").lower()
    sender_domain = report.get("sender_domain", "")
    reply_to_domain = report.get("reply_to_domain", "")

    auth_results = " ".join(str(headers.get(key, "")) for key in ["Authentication-Results", "Received-SPF", "ARC-Authentication-Results"]).lower()
    if "spf=fail" in auth_results or "spf fail" in auth_results:
        add_signal("SPF fail", "The SPF check failed for this message.", 18, "high")
    if "dkim=fail" in auth_results or "dkim fail" in auth_results:
        add_signal("DKIM fail", "The DKIM check failed for this message.", 18, "high")
    if "dmarc=fail" in auth_results or "dmarc fail" in auth_results:
        add_signal("DMARC fail", "The DMARC check failed for this message.", 22, "critical")

    if sender_domain and reply_to_domain and sender_domain != reply_to_domain:
        add_signal(
            "Reply-To mismatch",
            f"From domain {sender_domain} and Reply-To domain {reply_to_domain} do not match.",
            10,
            "medium",
        )

    x_mailer = str(headers.get("X-Mailer", ""))
    if x_mailer and any(token in x_mailer.lower() for token in ["python", "php", "powershell", "mailer"]):
        add_signal("Unusual mailer", f"X-Mailer: {x_mailer}", 6, "low")

    if "http://" in body_text:
        add_signal("Unencrypted links", "HTTP links were found in the body.", 10, "medium")

    keyword_hits = sorted({keyword for keyword in SUSPICIOUS_KEYWORDS if keyword in body_text})
    if keyword_hits:
        add_signal(
            "Suspicious keywords",
            ", ".join(keyword_hits[:8]),
            min(5 + len(keyword_hits) * 3, 18),
            "medium",
        )

    url_score = 0
    for url_item in report.get("urls", []):
        host = url_item.get("host", "")
        href = url_item.get("url", "")
        url_points = 0
        reasons = []

        if host_is_ip(host):
            url_points += 20
            reasons.append("IP address in URL")
        if host in URL_SHORTENERS:
            url_points += 12
            reasons.append("URL shortener")
        if "xn--" in host:
            url_points += 12
            reasons.append("punycode domain")
        if looks_suspicious_tld(host):
            url_points += 8
            reasons.append("unusual TLD")
        if sender_domain and not domain_matches(sender_domain, host):
            url_points += 8
            reasons.append("domain mismatch vs sender")

        if url_item.get("source") == "html" and url_item.get("text"):
            visible_host = extract_visible_host(url_item.get("text", ""))
            if visible_host and visible_host not in host and visible_host != sender_domain:
                url_points += 10
                reasons.append("visible link text differs from target")

        if url_points:
            url_score += url_points
            add_signal(
                "Suspicious link",
                f"{href} | {', '.join(reasons)}",
                min(url_points, 22),
                "high" if url_points >= 15 else "medium",
            )

    attachment_score = 0
    for attachment in report.get("attachments", []):
        extension = str(attachment.get("extension", "")).lower()
        name = attachment.get("name", "")
        attachment_points = 0
        reasons = []
        if extension in SUSPICIOUS_EXTENSIONS:
            attachment_points += 22
            reasons.append("executable file")
        if extension in MACRO_EXTENSIONS:
            attachment_points += 16
            reasons.append("office macro")
        if extension in ARCHIVE_EXTENSIONS:
            attachment_points += 6
            reasons.append("archive")
        if int(attachment.get("size", 0) or 0) > 8 * 1024 * 1024:
            attachment_points += 8
            reasons.append("large attachment")

        if attachment_points:
            attachment_score += attachment_points
            add_signal(
                "Suspicious attachment",
                f"{name} | {', '.join(reasons)}",
                min(attachment_points, 24),
                "high" if attachment_points >= 18 else "medium",
            )

    if sender_domain and sender_domain.count("-") >= 2:
        add_signal("Lookalike domain", f"Sender: {report.get('from_email', '')}", 8, "low")

    normalized_score = min(100, score + min(url_score // 2, 16) + min(attachment_score // 2, 16))
    return {
        "score": normalized_score,
        "signals": [signal.to_dict() for signal in signals],
        "categories": categories,
    }
