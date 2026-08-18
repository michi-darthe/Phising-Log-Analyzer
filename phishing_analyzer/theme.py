from dataclasses import dataclass


@dataclass(frozen=True)
class ThemeTokens:
    name: str
    page_bg: str
    page_bg_alt: str
    sidebar_bg: str
    card_bg: str
    card_soft: str
    border: str
    text: str
    muted: str
    accent: str
    accent_2: str
    warning: str
    danger: str
    success: str
    shadow: str
    hero_glow: str
    table_bg: str
    input_bg: str
    input_text: str
    button_bg: str
    button_text: str
    tab_bg: str


def get_theme(mode: str) -> ThemeTokens:
    normalized = (mode or "dark").strip().lower()
    if normalized == "light":
        return ThemeTokens(
            name="light",
            page_bg="#f4f7fb",
            page_bg_alt="#eaf1fb",
            sidebar_bg="rgba(255, 255, 255, 0.92)",
            card_bg="rgba(255, 255, 255, 0.92)",
            card_soft="rgba(241, 246, 252, 0.95)",
            border="rgba(148, 163, 184, 0.22)",
            text="#102033",
            muted="#5b6b82",
            accent="#0ea5e9",
            accent_2="#2563eb",
            warning="#b45309",
            danger="#be123c",
            success="#15803d",
            shadow="0 18px 45px rgba(15, 23, 42, 0.08)",
            hero_glow="radial-gradient(circle at top left, rgba(14, 165, 233, 0.16), transparent 30%), radial-gradient(circle at top right, rgba(37, 99, 235, 0.13), transparent 28%)",
            table_bg="rgba(255, 255, 255, 0.92)",
            input_bg="rgba(255, 255, 255, 0.96)",
            input_text="#102033",
            button_bg="linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%)",
            button_text="#ffffff",
            tab_bg="rgba(255, 255, 255, 0.9)",
        )

    return ThemeTokens(
        name="dark",
        page_bg="#06111f",
        page_bg_alt="#0a1729",
        sidebar_bg="rgba(7, 13, 24, 0.94)",
        card_bg="rgba(11, 20, 36, 0.9)",
        card_soft="rgba(15, 25, 45, 0.95)",
        border="rgba(148, 163, 184, 0.18)",
        text="#e5eefb",
        muted="#9fb0c7",
        accent="#67e8f9",
        accent_2="#38bdf8",
        warning="#fbbf24",
        danger="#fb7185",
        success="#4ade80",
        shadow="0 20px 52px rgba(0, 0, 0, 0.34)",
        hero_glow="radial-gradient(circle at top left, rgba(34, 211, 238, 0.18), transparent 32%), radial-gradient(circle at top right, rgba(59, 130, 246, 0.16), transparent 30%)",
        table_bg="rgba(8, 15, 29, 0.94)",
        input_bg="rgba(8, 15, 29, 0.96)",
        input_text="#e5eefb",
        button_bg="linear-gradient(135deg, #22d3ee 0%, #0ea5e9 100%)",
        button_text="#06111f",
        tab_bg="rgba(11, 20, 36, 0.9)",
    )


def build_css(tokens: ThemeTokens) -> str:
    return f"""
<style>
    html, body, [class*="css"] {{
        font-family: "Aptos", "Segoe UI", "SF Pro Display", "Helvetica Neue", sans-serif;
    }}

    .stApp {{
        background:
            {tokens.hero_glow},
            linear-gradient(180deg, {tokens.page_bg} 0%, {tokens.page_bg_alt} 100%);
        color: {tokens.text};
    }}

    [data-testid="stSidebar"] {{
        background: {tokens.sidebar_bg};
        border-right: 1px solid {tokens.border};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .hero {{
        position: relative;
        overflow: hidden;
        padding: 1.5rem 1.6rem;
        border-radius: 28px;
        border: 1px solid {tokens.border};
        background: linear-gradient(135deg, {tokens.card_bg}, {tokens.card_soft});
        box-shadow: {tokens.shadow};
        margin-bottom: 1rem;
    }}

    .hero::after {{
        content: "";
        position: absolute;
        inset: auto -40px -40px auto;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(14, 165, 233, 0.18), transparent 68%);
        pointer-events: none;
    }}

    .eyebrow {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        border: 1px solid rgba(14, 165, 233, 0.24);
        background: rgba(14, 165, 233, 0.08);
        color: {tokens.accent};
        font-size: 0.77rem;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }}

    .hero h1 {{
        margin: 0.75rem 0 0.45rem 0;
        color: {tokens.text};
        font-size: clamp(2rem, 3vw, 3rem);
        line-height: 1.02;
        max-width: 14ch;
    }}

    .hero p {{
        margin: 0;
        max-width: 62rem;
        color: {tokens.muted};
        font-size: 1.02rem;
        line-height: 1.6;
    }}

    .hero-meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 1rem;
    }}

    .brand-mark {{
        display: inline-flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.55rem;
    }}

    .brand-logo {{
        display: inline-flex;
        align-items: center;
        margin-bottom: 0.55rem;
    }}

    .brand-logo__img {{
        height: 3.35rem;
        width: auto;
        max-width: 14rem;
        object-fit: contain;
        border-radius: 0.8rem;
        box-shadow: {tokens.shadow};
        border: 1px solid {tokens.border};
        background: rgba(255, 255, 255, 0.05);
        padding: 0.3rem 0.45rem;
    }}

    .brand-mark__icon {{
        width: 3rem;
        height: 3rem;
        border-radius: 0.95rem;
        display: grid;
        place-items: center;
        color: {tokens.button_text};
        background: {tokens.button_bg};
        box-shadow: {tokens.shadow};
        border: 1px solid rgba(14, 165, 233, 0.22);
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: 0.06em;
    }}

    .brand-mark__text {{
        display: grid;
        gap: 0.1rem;
    }}

    .brand-mark__name {{
        color: {tokens.text};
        font-size: 1rem;
        font-weight: 750;
        letter-spacing: 0.02em;
    }}

    .brand-mark__sub {{
        color: {tokens.muted};
        font-size: 0.82rem;
    }}

    .pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.4rem 0.75rem;
        border-radius: 999px;
        border: 1px solid {tokens.border};
        background: rgba(15, 23, 42, 0.06);
        color: {tokens.text};
        font-size: 0.8rem;
    }}

    .pill-danger {{ border-color: rgba(251, 113, 133, 0.24); color: {tokens.danger}; background: rgba(251, 113, 133, 0.08); }}
    .pill-warning {{ border-color: rgba(251, 191, 36, 0.24); color: {tokens.warning}; background: rgba(251, 191, 36, 0.08); }}
    .pill-success {{ border-color: rgba(74, 222, 128, 0.24); color: {tokens.success}; background: rgba(74, 222, 128, 0.08); }}
    .pill-info {{ border-color: rgba(103, 232, 249, 0.24); color: {tokens.accent}; background: rgba(103, 232, 249, 0.08); }}

    .panel {{
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        border-radius: 24px;
        padding: 1rem;
    }}

    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.9rem;
        margin: 1rem 0 1.2rem 0;
    }}

    .feature-card {{
        border: 1px solid {tokens.border};
        background: linear-gradient(180deg, {tokens.card_bg}, {tokens.card_soft});
        box-shadow: {tokens.shadow};
        border-radius: 22px;
        padding: 1rem 1.05rem;
        min-height: 122px;
    }}

    .feature-card h3, .section-title {{
        margin: 0;
        color: {tokens.text};
        font-size: 1rem;
        font-weight: 650;
    }}

    .feature-card p {{
        margin: 0.35rem 0 0 0;
        color: {tokens.muted};
        line-height: 1.5;
        font-size: 0.94rem;
    }}

    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.8rem;
    }}

    .kpi {{
        border: 1px solid {tokens.border};
        background: linear-gradient(180deg, {tokens.card_bg}, {tokens.card_soft});
        border-radius: 22px;
        padding: 1rem 1.05rem;
        box-shadow: {tokens.shadow};
    }}

    .kpi-label {{
        color: {tokens.muted};
        font-size: 0.8rem;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }}

    .kpi-value {{
        color: {tokens.text};
        font-size: 1.85rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }}

    .kpi-hint {{
        color: {tokens.muted};
        font-size: 0.88rem;
        margin-top: 0.2rem;
    }}

    .signal-list {{
        display: grid;
        gap: 0.75rem;
    }}

    .finding-summary {{
        border: 1px solid {tokens.border};
        background: linear-gradient(180deg, {tokens.card_bg}, {tokens.card_soft});
        box-shadow: {tokens.shadow};
        border-radius: 20px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.85rem;
    }}

    .finding-summary__header {{
        color: {tokens.text};
        font-size: 0.83rem;
        text-transform: uppercase;
        letter-spacing: 0.11em;
        margin-bottom: 0.6rem;
    }}

    .finding-summary__badges {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
    }}

    .signal {{
        border: 1px solid {tokens.border};
        background: linear-gradient(180deg, {tokens.card_bg}, {tokens.card_soft});
        box-shadow: {tokens.shadow};
        border-radius: 20px;
        padding: 0.95rem 1rem;
    }}

    .signal-top {{
        display: flex;
        justify-content: space-between;
        gap: 0.75rem;
        align-items: start;
    }}

    .signal-title {{
        color: {tokens.text};
        font-weight: 650;
        margin: 0;
    }}

    .signal-detail {{
        color: {tokens.muted};
        margin: 0.3rem 0 0 0;
        font-size: 0.92rem;
        line-height: 1.45;
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;
        min-width: 90px;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.79rem;
        border: 1px solid {tokens.border};
    }}

    .badge-critical, .badge-high {{ color: {tokens.danger}; background: rgba(251, 113, 133, 0.09); border-color: rgba(251, 113, 133, 0.2); }}
    .badge-medium {{ color: {tokens.warning}; background: rgba(251, 191, 36, 0.08); border-color: rgba(251, 191, 36, 0.2); }}
    .badge-low {{ color: {tokens.accent}; background: rgba(103, 232, 249, 0.08); border-color: rgba(103, 232, 249, 0.2); }}

    .report-grid {{
        display: grid;
        grid-template-columns: 1.3fr 0.7fr;
        gap: 1rem;
    }}

    .callout {{
        border: 1px solid {tokens.border};
        border-radius: 22px;
        background: linear-gradient(135deg, {tokens.card_bg}, {tokens.card_soft});
        box-shadow: {tokens.shadow};
        padding: 1rem;
    }}

    .callout h3 {{
        margin: 0 0 0.35rem 0;
        color: {tokens.text};
        font-size: 1rem;
    }}

    .callout p {{
        margin: 0;
        color: {tokens.muted};
        line-height: 1.55;
    }}

    .stAlert {{
        border-radius: 18px;
    }}

    .stDataFrame, .stTable, .stJson, .stCodeBlock {{
        border-radius: 18px;
        overflow: hidden;
    }}

    div[data-baseweb="input"], div[data-baseweb="select"], textarea, input {{
        background: {tokens.input_bg} !important;
        color: {tokens.input_text} !important;
    }}

    .stButton > button, .stDownloadButton > button {{
        border-radius: 14px;
        border: 1px solid rgba(14, 165, 233, 0.25);
        background: {tokens.button_bg};
        color: {tokens.button_text};
        font-weight: 650;
        padding: 0.65rem 1rem;
    }}

    .stButton > button:hover, .stDownloadButton > button:hover {{
        filter: brightness(1.02);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.4rem;
        background: transparent;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 999px;
        padding: 0.55rem 0.9rem;
        background: {tokens.tab_bg};
        color: {tokens.muted};
        border: 1px solid {tokens.border};
    }}

    .stTabs [aria-selected="true"] {{
        background: rgba(14, 165, 233, 0.12);
        color: {tokens.text};
        border-color: rgba(14, 165, 233, 0.22);
    }}

    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {{
        color: {tokens.text};
    }}

    .sidebar-card {{
        border: 1px solid {tokens.border};
        background: linear-gradient(180deg, {tokens.card_bg}, {tokens.card_soft});
        border-radius: 20px;
        padding: 0.9rem;
        box-shadow: {tokens.shadow};
    }}

    @media (max-width: 960px) {{
        .feature-grid, .kpi-grid, .report-grid {{
            grid-template-columns: 1fr;
        }}
    }}
</style>
"""
