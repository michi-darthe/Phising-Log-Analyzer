import base64
from typing import Any

import requests
import streamlit as st


def vt_summary_from_attributes(attributes: dict[str, Any]) -> dict[str, Any]:
    stats = attributes.get("last_analysis_stats", {}) or {}
    total = sum(int(value) for value in stats.values() if isinstance(value, (int, float)))
    return {
        "stats": stats,
        "total": total,
        "malicious": int(stats.get("malicious", 0)),
        "suspicious": int(stats.get("suspicious", 0)),
        "harmless": int(stats.get("harmless", 0)),
        "permalink": attributes.get("permalink", ""),
        "meaningful_name": attributes.get("meaningful_name", ""),
    }


@st.cache_data(ttl=1800, show_spinner=False)
def query_virustotal_url(api_key: str, url: str) -> dict[str, Any]:
    url_id = base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8").strip("=")
    response = requests.get(
        f"https://www.virustotal.com/api/v3/urls/{url_id}",
        headers={"x-apikey": api_key},
        timeout=20,
    )
    response.raise_for_status()
    return response.json().get("data", {}).get("attributes", {})


@st.cache_data(ttl=1800, show_spinner=False)
def query_virustotal_ip(api_key: str, ip_address_value: str) -> dict[str, Any]:
    response = requests.get(
        f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address_value}",
        headers={"x-apikey": api_key},
        timeout=20,
    )
    response.raise_for_status()
    return response.json().get("data", {}).get("attributes", {})


@st.cache_data(ttl=1800, show_spinner=False)
def query_virustotal_file(api_key: str, sha256_hash: str) -> dict[str, Any]:
    response = requests.get(
        f"https://www.virustotal.com/api/v3/files/{sha256_hash}",
        headers={"x-apikey": api_key},
        timeout=20,
    )
    response.raise_for_status()
    return response.json().get("data", {}).get("attributes", {})

