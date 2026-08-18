import html as html_lib
import json
import os
import ipaddress
from base64 import b64encode
from pathlib import Path
from textwrap import dedent
from typing import Any

import streamlit as st

from .config import APP_NAME, APP_SUBTITLE, SAFE_ACTION_HINTS
from .parsing import parse_email_bytes, parse_image_upload
from .scoring import score_report
from .theme import build_css, get_theme
from .virustotal import query_virustotal_file, query_virustotal_ip, query_virustotal_url, vt_summary_from_attributes


ASSET_CANDIDATES = [
    "mm_group.jpg",
    "mm_group.jpeg",
    "mm_group.png",
    "mm_group.webp",
    "mm-group-logo.jpg",
    "mm-group-logo.jpeg",
    "mm-group-logo.png",
    "mm-group-logo.webp",
    "mm_logo.jpg",
    "mm_logo.jpeg",
    "logo.jpg",
    "logo.jpeg",
    "logo.png",
    "brand.jpg",
    "brand.jpeg",
    "brand.png",
]


def _status_pill(label: str, kind: str) -> str:
    return f'<span class="pill pill-{kind}">{html_lib.escape(label)}</span>'


def _mm_brand_mark() -> str:
    return """
    <div class="brand-mark">
        <div class="brand-mark__icon">
            <span>MM</span>
        </div>
        <div class="brand-mark__text">
            <div class="brand-mark__name">MM Group</div>
            <div class="brand-mark__sub">Mayr-Melnhof</div>
        </div>
    </div>
    """


def _find_logo_path() -> Path | None:
    project_root = Path(__file__).resolve().parents[1]
    for candidate in ASSET_CANDIDATES:
        candidate_path = project_root / candidate
        if candidate_path.is_file():
            return candidate_path
    for candidate_path in sorted(project_root.glob("*")):
        stem = candidate_path.stem.lower()
        if candidate_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".svg"} and (
            "logo" in stem or "mm" in stem or "group" in stem
        ):
            return candidate_path
    return None


def _logo_markup() -> str:
    logo_path = _find_logo_path()
    if not logo_path:
        return _mm_brand_mark()

    if logo_path.suffix.lower() == ".svg":
        try:
            data = logo_path.read_bytes()
        except Exception:
            return _mm_brand_mark()
        encoded = b64encode(data).decode("ascii")
        return f"""
        <div class="brand-logo">
            <img class="brand-logo__img" src="data:image/svg+xml;base64,{encoded}" alt="MM Group logo" />
        </div>
        """

    try:
        data = logo_path.read_bytes()
    except Exception:
        return _mm_brand_mark()

    encoded = b64encode(data).decode("ascii")
    mime = "image/png" if logo_path.suffix.lower() == ".png" else "image/webp" if logo_path.suffix.lower() == ".webp" else "image/jpeg"
    return f"""
    <div class="brand-logo">
        <img class="brand-logo__img" src="data:{mime};base64,{encoded}" alt="MM Group logo" />
    </div>
    """


def _metric_card(label: str, value: str, hint: str) -> str:
    return f"""
    <div class="kpi">
        <div class="kpi-label">{html_lib.escape(label)}</div>
        <div class="kpi-value">{html_lib.escape(value)}</div>
        <div class="kpi-hint">{html_lib.escape(hint)}</div>
    </div>
    """


def _render_header(tokens) -> None:
    logo_path = _find_logo_path()
    left, right = st.columns([0.22, 0.78], gap="large")

    with left:
        if logo_path:
            st.image(str(logo_path), use_container_width=True)
        else:
            st.markdown(_logo_markup(), unsafe_allow_html=True)

    with right:
        st.markdown(
            dedent(
                f"""
                <div class="hero">
                    <span class="eyebrow">Internal Security Intake</span>
                    <h1>{html_lib.escape(APP_NAME)}</h1>
                    <p>{html_lib.escape(APP_SUBTITLE)}</p>
                    <div class="hero-meta">
                        {_status_pill("Header analysis", "info")}
                        {_status_pill("Attachment scan", "info")}
                        {_status_pill("URL reputation", "info")}
                        {_status_pill("JSON export", "info")}
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )


def _render_feature_cards() -> None:
    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature-card">
                <h3>Clean intake flow</h3>
                <p>Employees can upload .eml files or screenshots without losing header and body context.</p>
            </div>
            <div class="feature-card">
                <h3>Smart risk model</h3>
                <p>SPF, DKIM, DMARC, Reply-To mismatch, suspicious keywords, URL tricks, and risky attachments are scored together.</p>
            </div>
            <div class="feature-card">
                <h3>Operational export</h3>
                <p>Every report can be downloaded as JSON for handoff, logging, or later automation.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_top_metrics(score: int, report: dict[str, Any], analysis: dict[str, Any]) -> None:
    metric_cols = st.columns(4)
    metrics = [
        ("Risk score", f"{score}/100", "Heuristic output"),
        ("Links", str(len(report.get("urls", []))), "Extracted URLs"),
        ("Attachments", str(len(report.get("attachments", []))), "Attachment inventory"),
        ("Signals", str(len(analysis.get("signals", []))), "Detected findings"),
    ]
    for column, metric in zip(metric_cols, metrics, strict=False):
        with column:
            st.markdown(_metric_card(*metric), unsafe_allow_html=True)


def _normalize_priority(score: int) -> tuple[str, str]:
    if score >= 70:
        return "critical", "High priority"
    if score >= 35:
        return "medium", "Review recommended"
    return "low", "Low priority"


def _render_banner(score: int) -> None:
    kind, label = _normalize_priority(score)
    if kind == "critical":
        st.error(f"{label}: score {score}/100. The message shows clear phishing indicators.")
    elif kind == "medium":
        st.warning(f"{label}: score {score}/100. Several indicators need a manual review.")
    else:
        st.success(f"{label}: score {score}/100. Only a few weak signals were found.")


def _render_signals(signals: list[dict[str, Any]]) -> None:
    if not signals:
        st.info("No relevant signals were found.")
        return

    html_blocks = []
    for signal in signals:
        severity = signal.get("severity", "low")
        badge_kind = "critical" if severity == "critical" else severity
        html_blocks.append(
            f"""
            <div class="signal">
                <div class="signal-top">
                    <div>
                        <div class="signal-title">{html_lib.escape(str(signal.get('title', '')))}</div>
                        <div class="signal-detail">{html_lib.escape(str(signal.get('detail', '')))}</div>
                    </div>
                    <span class="badge badge-{badge_kind}">{html_lib.escape(str(signal.get('points', 0)))} points</span>
                </div>
            </div>
            """
        )

    st.markdown('<div class="signal-list">' + "".join(html_blocks) + "</div>", unsafe_allow_html=True)


def _render_findings_table(signals: list[dict[str, Any]]) -> None:
    if not signals:
        st.info("No findings to summarize yet.")
        return

    rows = []
    for index, signal in enumerate(signals, start=1):
        severity = str(signal.get("severity", "low"))
        points = int(signal.get("points", 0) or 0)
        rows.append(
            {
                "#": index,
                "Finding": signal.get("title", ""),
                "Severity": severity.title(),
                "Points": points,
                "What to check": signal.get("detail", ""),
            }
        )

    st.dataframe(rows, use_container_width=True, hide_index=True)


def _render_finding_summary(signals: list[dict[str, Any]]) -> None:
    if not signals:
        return

    grouped = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for signal in signals:
        severity = str(signal.get("severity", "low"))
        grouped[severity if severity in grouped else "low"] += 1

    severity_class = {"critical": "danger", "high": "danger", "medium": "warning", "low": "info"}
    badges = "".join(
        f'<span class="pill pill-{severity_class.get(severity, "info")}">{severity.title()}: {count}</span>'
        for severity, count in grouped.items()
        if count
    )
    st.markdown(
        f"""
        <div class="finding-summary">
            <div class="finding-summary__header">Suspicious pattern overview</div>
            <div class="finding-summary__badges">{badges}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_detail_table(report: dict[str, Any]) -> None:
    details = [
        ("From name", report.get("from_name", "") or "Unknown"),
        ("From email", report.get("from_email", "") or "Unknown"),
        ("Reply-To name", report.get("reply_to_name", "") or "Not set"),
        ("Reply-To email", report.get("reply_to_email", "") or "Not set"),
        ("Subject", report.get("subject", "") or "No subject"),
        ("Date", report.get("date", "") or "Unknown"),
        ("Sender domain", report.get("sender_domain", "") or "Unknown"),
        ("Message size", f"{int(report.get('raw_size', 0)):,} bytes".replace(",", ".")),
    ]
    st.dataframe([{"Field": key, "Value": value} for key, value in details], use_container_width=True, hide_index=True)


def _render_url_table(report: dict[str, Any]) -> None:
    urls = report.get("urls", [])
    if urls:
        st.dataframe(
            [
                {
                    "URL": item.get("url", ""),
                    "Host": item.get("host", ""),
                    "Source": item.get("source", ""),
                    "Visible text": item.get("text", ""),
                }
                for item in urls
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No links were found.")


def _render_attachment_table(report: dict[str, Any]) -> None:
    attachments = report.get("attachments", [])
    if attachments:
        st.dataframe(
            [
                {
                    "Name": item.get("name", ""),
                    "Type": item.get("content_type", ""),
                    "Size": f"{int(item.get('size', 0)):,} bytes".replace(",", "."),
                    "SHA256": (item.get("sha256", "") or "")[:16] + ("..." if item.get("sha256") else ""),
                }
                for item in attachments
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No attachments were found.")


def _serialize_payload(report: dict[str, Any], analysis: dict[str, Any], vt_results: dict[str, Any]) -> str:
    return json.dumps({"report": report, "analysis": analysis, "virustotal": vt_results}, indent=2, ensure_ascii=False)


def _collect_virustotal(api_key: str, report: dict[str, Any]) -> dict[str, Any]:
    if not api_key:
        return {}

    results: dict[str, Any] = {"urls": [], "ips": [], "files": []}
    for url_item in report.get("urls", [])[:4]:
        url_value = url_item.get("url", "")
        host = url_item.get("host", "")
        if not url_value:
            continue
        try:
            results["urls"].append({"url": url_value, **vt_summary_from_attributes(query_virustotal_url(api_key, url_value))})
        except Exception as exc:
            results["urls"].append({"url": url_value, "error": str(exc)})

        try:
            ipaddress.ip_address(host)
        except ValueError:
            continue
        else:
            try:
                results["ips"].append({"ip": host, **vt_summary_from_attributes(query_virustotal_ip(api_key, host))})
            except Exception as exc:
                results["ips"].append({"ip": host, "error": str(exc)})

    for attachment in report.get("attachments", [])[:4]:
        sha256_hash = attachment.get("sha256", "")
        if not sha256_hash:
            continue
        try:
            results["files"].append({"file": attachment.get("name", ""), **vt_summary_from_attributes(query_virustotal_file(api_key, sha256_hash))})
        except Exception as exc:
            results["files"].append({"file": attachment.get("name", ""), "error": str(exc)})

    return results


def run_app() -> None:
    st.set_page_config(page_title=APP_NAME, page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

    theme_mode = st.sidebar.selectbox("Theme", ["Dark", "Light"], index=0, help="Switch the dashboard appearance.")
    tokens = get_theme(theme_mode)
    st.markdown(build_css(tokens), unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-card">
                <div class="section-title">Configuration</div>
                <p style="margin:0.4rem 0 0 0; color:{tokens.muted}; line-height:1.5;">
                    Tune the scan behaviour and optionally connect VirusTotal for external reputation checks.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        api_key = st.text_input("VirusTotal API key", value=os.getenv("VIRUSTOTAL_API_KEY", ""), type="password")
        use_ocr = st.toggle("Enable OCR for images", value=True)
        sensitivity = st.select_slider("Sensitivity", options=["Balanced", "Strict", "Max"], value="Balanced")
        st.markdown(
            """
            <div class="sidebar-card" style="margin-top:0.75rem;">
                <div class="section-title">Response hints</div>
                <div style="margin-top:0.5rem; display:grid; gap:0.45rem;">
                    <span class="pill pill-info">Isolate suspicious mail</span>
                    <span class="pill pill-warning">Do not open risky attachments</span>
                    <span class="pill pill-success">Share the JSON report with SOC</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='margin-top:0.7rem; display:grid; gap:0.35rem;'>"
            + "".join(f"<div class='pill'>{html_lib.escape(hint)}</div>" for hint in SAFE_ACTION_HINTS)
            + "</div>",
            unsafe_allow_html=True,
        )

    _render_header(tokens)
    _render_feature_cards()

    uploaded_file = st.file_uploader(
        "Upload suspicious email or screenshot",
        type=["eml", "png", "jpg", "jpeg"],
        accept_multiple_files=False,
        help="Upload a forwarded .eml file or a screenshot of the suspicious message.",
    )

    if not uploaded_file:
        st.info("Upload a file to start the analysis.")
        return

    file_name = (uploaded_file.name or "").lower()
    report = parse_email_bytes(uploaded_file.getvalue()) if file_name.endswith(".eml") else parse_image_upload(uploaded_file, use_ocr)
    analysis = score_report(report)

    score = analysis["score"]
    if sensitivity == "Strict":
        score = min(100, int(score * 1.1))
    elif sensitivity == "Max":
        score = min(100, int(score * 1.2))

    vt_results = _collect_virustotal(api_key, report)

    st.divider()
    _render_banner(score)
    _render_top_metrics(score, report, analysis)

    st.progress(min(score, 100))

    report_left, report_right = st.columns([1.35, 0.65], gap="large")
    with report_left:
        st.markdown('<div class="section-title">Findings</div>', unsafe_allow_html=True)
        _render_finding_summary(analysis.get("signals", []))
        _render_signals(analysis.get("signals", []))
        st.markdown('<div class="section-title" style="margin-top:1rem;">Findings table</div>', unsafe_allow_html=True)
        _render_findings_table(analysis.get("signals", []))
        st.markdown('<div class="section-title" style="margin-top:1rem;">Message details</div>', unsafe_allow_html=True)
        _render_detail_table(report)

    with report_right:
        st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
        st.download_button(
            "Download JSON report",
            data=_serialize_payload(report, analysis, vt_results),
            file_name="phishing-report.json",
            mime="application/json",
            use_container_width=True,
        )
        st.markdown(
            """
            <div class="callout" style="margin-top:0.9rem;">
                <h3>Recommended next step</h3>
                <p>Quarantine the email, warn the user, and validate any link or attachment in a controlled environment.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if vt_results:
            st.markdown('<div class="section-title" style="margin-top:0.9rem;">VirusTotal</div>', unsafe_allow_html=True)
            with st.expander("URLs"):
                st.json(vt_results.get("urls", []))
            with st.expander("IPs"):
                st.json(vt_results.get("ips", []))
            with st.expander("Files"):
                st.json(vt_results.get("files", []))

    tabs = st.tabs(["Links", "Attachments", "Headers", "Raw text"])
    with tabs[0]:
        _render_url_table(report)
    with tabs[1]:
        _render_attachment_table(report)
    with tabs[2]:
        if report.get("headers"):
            st.json(report["headers"])
        else:
            st.info("No headers available for this upload.")
    with tabs[3]:
        st.text(report.get("body_text", "") or "No extracted text available.")
