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
    normalized = (mode or "light").strip().lower()
    if normalized == "light":
        return ThemeTokens(
            name="light",
            page_bg="#f7f9fc",
            page_bg_alt="#eef3f8",
            sidebar_bg="rgba(255, 255, 255, 0.96)",
            card_bg="rgba(255, 255, 255, 0.98)",
            card_soft="rgba(248, 250, 252, 1.0)",
            border="rgba(148, 163, 184, 0.14)",
            text="#102033",
            muted="#5a6c82",
            accent="#0284c7",
            accent_2="#2563eb",
            warning="#a16207",
            danger="#be123c",
            success="#15803d",
            shadow="0 12px 28px rgba(15, 23, 42, 0.05)",
            hero_glow="radial-gradient(circle at top left, rgba(14, 165, 233, 0.06), transparent 24%), radial-gradient(circle at top right, rgba(37, 99, 235, 0.05), transparent 22%)",
            table_bg="rgba(255, 255, 255, 0.98)",
            input_bg="rgba(255, 255, 255, 1.0)",
            input_text="#102033",
            button_bg="linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%)",
            button_text="#ffffff",
            tab_bg="rgba(255, 255, 255, 0.98)",
        )

    return ThemeTokens(
        name="dark",
        page_bg="#04070c",
        page_bg_alt="#090f18",
        sidebar_bg="rgba(6, 10, 16, 0.96)",
        card_bg="rgba(10, 14, 22, 0.98)",
        card_soft="rgba(12, 18, 28, 0.99)",
        border="rgba(148, 163, 184, 0.10)",
        text="#f1f5fb",
        muted="#94a3b8",
        accent="#67e8f9",
        accent_2="#38bdf8",
        warning="#fbbf24",
        danger="#fb7185",
        success="#4ade80",
        shadow="0 16px 38px rgba(0, 0, 0, 0.24)",
        hero_glow="radial-gradient(circle at top left, rgba(34, 211, 238, 0.05), transparent 24%), radial-gradient(circle at top right, rgba(59, 130, 246, 0.05), transparent 22%)",
        table_bg="rgba(7, 11, 18, 0.99)",
        input_bg="rgba(7, 11, 18, 0.99)",
        input_text="#f1f5fb",
        button_bg="linear-gradient(135deg, #22d3ee 0%, #0ea5e9 100%)",
        button_text="#03101d",
        tab_bg="rgba(10, 14, 22, 0.98)",
    )


def build_css(tokens: ThemeTokens) -> str:
    color_scheme = "dark" if tokens.name == "dark" else "light"
    return f"""
<style>
    html, body, [class*="css"] {{
        font-family: "Aptos", "Segoe UI", "SF Pro Display", "Helvetica Neue", sans-serif;
        background: {tokens.page_bg};
        color: {tokens.text};
    }}

    html {{
        color-scheme: {color_scheme};
    }}

    body {{
        background:
            {tokens.hero_glow},
            linear-gradient(180deg, {tokens.page_bg} 0%, {tokens.page_bg_alt} 100%);
        color: {tokens.text};
    }}

    .stApp {{
        background:
            {tokens.hero_glow},
            linear-gradient(180deg, {tokens.page_bg} 0%, {tokens.page_bg_alt} 100%);
        color: {tokens.text};
        min-height: 100vh;
    }}

    main .block-container {{
        max-width: 1280px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }}

    [data-testid="stSidebar"] {{
        background: {tokens.sidebar_bg};
        border-right: 1px solid {tokens.border};
        box-shadow: 18px 0 50px rgba(0, 0, 0, 0.14);
        backdrop-filter: blur(18px);
    }}

    [data-testid="stSidebar"] * {{
        color: {tokens.text};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .hero {{
        position: relative;
        overflow: hidden;
        padding: 1.2rem 1.25rem;
        border-radius: 22px;
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        margin-bottom: 1rem;
    }}

    .hero::after {{
        content: "";
        position: absolute;
        inset: auto -32px -32px auto;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(14, 165, 233, 0.05), transparent 66%);
        pointer-events: none;
    }}

    .eyebrow {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        border: 1px solid rgba(14, 165, 233, 0.14);
        background: rgba(14, 165, 233, 0.04);
        color: {tokens.accent};
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }}

    .hero h1 {{
        margin: 0.65rem 0 0.35rem 0;
        color: {tokens.text};
        font-size: clamp(2rem, 3vw, 3.15rem);
        line-height: 0.98;
        max-width: 12ch;
        letter-spacing: -0.04em;
    }}

    .hero p {{
        margin: 0;
        max-width: 58rem;
        color: {tokens.muted};
        font-size: 0.96rem;
        line-height: 1.55;
    }}

    .hero-meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 1rem;
    }}

    .app-mark {{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.85rem;
        width: 100%;
        min-height: 10rem;
        padding: 1rem;
        border: 1px solid {tokens.border};
        border-radius: 22px;
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
    }}

    .app-mark__icon {{
        position: relative;
        width: 4.4rem;
        height: 4.4rem;
        flex: 0 0 4.4rem;
        border-radius: 1.2rem;
        display: grid;
        place-items: center;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(103, 232, 249, 0.12), rgba(14, 165, 233, 0.22));
        border: 1px solid rgba(103, 232, 249, 0.16);
        box-shadow: 0 14px 30px rgba(2, 132, 199, 0.12);
    }}

    .app-mark__ring {{
        position: absolute;
        inset: 0.55rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.34);
        box-shadow: inset 0 0 0 1px rgba(2, 132, 199, 0.10);
        opacity: 0.88;
    }}

    .app-mark__shield {{
        position: relative;
        width: 1.7rem;
        height: 2.1rem;
        background: linear-gradient(180deg, #ffffff 0%, #d7f6ff 100%);
        clip-path: polygon(50% 0%, 90% 16%, 90% 60%, 50% 100%, 10% 60%, 10% 16%);
        box-shadow: 0 0 24px rgba(255, 255, 255, 0.12);
    }}

    .app-mark__monogram {{
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
        color: #03101d;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        transform: translateY(0.02rem);
    }}

    .app-mark__shield::after {{
        content: "";
        position: absolute;
        left: 50%;
        top: 50%;
        width: 0.88rem;
        height: 0.16rem;
        border-radius: 999px;
        transform: translate(-50%, -50%) rotate(-38deg);
        background: linear-gradient(90deg, rgba(2, 132, 199, 0.9), rgba(14, 165, 233, 0.95));
        box-shadow: 0 0 14px rgba(14, 165, 233, 0.5);
    }}

    .app-mark__spark {{
        position: absolute;
        right: 0.42rem;
        top: 0.42rem;
        width: 0.38rem;
        height: 0.38rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 0 14px rgba(255, 255, 255, 0.6);
    }}

    .app-mark__text {{
        display: grid;
        gap: 0.15rem;
        min-width: 0;
    }}

    .app-mark__name {{
        color: {tokens.text};
        font-size: 1.05rem;
        font-weight: 780;
        letter-spacing: -0.02em;
        line-height: 1.15;
    }}

    .app-mark__sub {{
        color: {tokens.muted};
        font-size: 0.78rem;
        line-height: 1.35;
    }}

    .pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.38rem 0.72rem;
        border-radius: 999px;
        border: 1px solid {tokens.border};
        background: rgba(148, 163, 184, 0.06);
        color: {tokens.text};
        font-size: 0.77rem;
    }}

    .pill-danger {{ border-color: rgba(251, 113, 133, 0.24); color: {tokens.danger}; background: rgba(251, 113, 133, 0.08); }}
    .pill-warning {{ border-color: rgba(251, 191, 36, 0.24); color: {tokens.warning}; background: rgba(251, 191, 36, 0.08); }}
    .pill-success {{ border-color: rgba(74, 222, 128, 0.24); color: {tokens.success}; background: rgba(74, 222, 128, 0.08); }}
    .pill-info {{ border-color: rgba(103, 232, 249, 0.24); color: {tokens.accent}; background: rgba(103, 232, 249, 0.08); }}

    .panel {{
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        border-radius: 20px;
        padding: 0.95rem;
    }}

    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.85rem;
        margin: 0.8rem 0 1rem 0;
    }}

    .feature-card {{
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        border-radius: 20px;
        padding: 0.95rem 1rem;
        min-height: 104px;
    }}

    .feature-card h3, .section-title {{
        margin: 0;
        color: {tokens.text};
        font-size: 0.95rem;
        font-weight: 700;
    }}

    .feature-card p {{
        margin: 0.35rem 0 0 0;
        color: {tokens.muted};
        line-height: 1.5;
        font-size: 0.9rem;
    }}

    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.8rem;
    }}

    .kpi {{
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        border-radius: 18px;
        padding: 0.95rem 1rem;
        box-shadow: {tokens.shadow};
    }}

    .kpi-label {{
        color: {tokens.muted};
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }}

    .kpi-value {{
        color: {tokens.text};
        font-size: 1.7rem;
        font-weight: 700;
        margin-top: 0.18rem;
    }}

    .kpi-hint {{
        color: {tokens.muted};
        font-size: 0.82rem;
        margin-top: 0.2rem;
    }}

    .signal-list {{
        display: grid;
        gap: 0.65rem;
    }}

    .finding-summary {{
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        border-radius: 18px;
        padding: 0.85rem 0.95rem;
        margin-bottom: 0.75rem;
    }}

    .finding-summary__header {{
        color: {tokens.text};
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.6rem;
    }}

    .finding-summary__badges {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
    }}

    .signal {{
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        border-radius: 16px;
        padding: 0.88rem 0.95rem;
    }}

    .signal-top {{
        display: flex;
        justify-content: space-between;
        gap: 0.75rem;
        align-items: start;
    }}

    .signal-title {{
        color: {tokens.text};
        font-weight: 700;
        margin: 0;
    }}

    .signal-detail {{
        color: {tokens.muted};
        margin: 0.3rem 0 0 0;
        font-size: 0.88rem;
        line-height: 1.48;
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;
        min-width: 86px;
        padding: 0.33rem 0.68rem;
        border-radius: 999px;
        font-size: 0.76rem;
        border: 1px solid {tokens.border};
    }}

    .badge-critical, .badge-high {{ color: {tokens.danger}; background: rgba(251, 113, 133, 0.09); border-color: rgba(251, 113, 133, 0.2); }}
    .badge-medium {{ color: {tokens.warning}; background: rgba(251, 191, 36, 0.08); border-color: rgba(251, 191, 36, 0.2); }}
    .badge-low {{ color: {tokens.accent}; background: rgba(103, 232, 249, 0.08); border-color: rgba(103, 232, 249, 0.2); }}

    .report-grid {{
        display: grid;
        grid-template-columns: 1.3fr 0.7fr;
        gap: 0.9rem;
    }}

    .callout {{
        border: 1px solid {tokens.border};
        border-radius: 18px;
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        padding: 0.95rem;
    }}

    .callout h3 {{
        margin: 0 0 0.35rem 0;
        color: {tokens.text};
        font-size: 0.95rem;
    }}

    .callout p {{
        margin: 0;
        color: {tokens.muted};
        line-height: 1.5;
        font-size: 0.9rem;
    }}

    .stAlert {{
        border-radius: 14px;
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        color: {tokens.text};
    }}

    .stDataFrame, .stTable, .stJson, .stCodeBlock {{
        border-radius: 18px;
        overflow: hidden;
    }}

    div[data-testid="stDataFrame"], div[data-testid="stTable"], div[data-testid="stJson"], div[data-testid="stCodeBlock"] {{
        background: {tokens.table_bg};
        border: 1px solid {tokens.border};
        box-shadow: {tokens.shadow};
    }}

    div[data-testid="stDataFrame"] [role="grid"],
    div[data-testid="stDataFrame"] [role="row"],
    div[data-testid="stDataFrame"] [role="columnheader"],
    div[data-testid="stDataFrame"] [role="gridcell"],
    div[data-testid="stTable"] table,
    div[data-testid="stTable"] th,
    div[data-testid="stTable"] td {{
        background: {tokens.table_bg} !important;
        color: {tokens.text} !important;
        border-color: {tokens.border} !important;
    }}

    div[data-testid="stJson"] pre, div[data-testid="stCodeBlock"] pre {{
        background: {tokens.table_bg} !important;
        color: {tokens.text} !important;
    }}

    section[data-testid="stFileUploaderDropzone"] {{
        background: {tokens.card_bg};
        border: 1px dashed rgba(14, 165, 233, 0.22);
        border-radius: 18px;
        padding: 1.1rem;
        box-shadow: {tokens.shadow};
    }}

    section[data-testid="stFileUploaderDropzone"] *,
    section[data-testid="stFileUploaderDropzone"] label {{
        color: {tokens.text};
    }}

    section[data-testid="stFileUploaderDropzone"] > div {{
        background: transparent;
    }}

    section[data-testid="stFileUploaderDropzone"] button {{
        background: {tokens.card_soft};
        color: {tokens.text};
        border: 1px solid {tokens.border};
    }}

    div[data-baseweb="input"], div[data-baseweb="select"], textarea, input {{
        background: {tokens.input_bg} !important;
        color: {tokens.input_text} !important;
    }}

    div[data-baseweb="base-input"] {{
        background: {tokens.input_bg} !important;
        border: 1px solid {tokens.border} !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }}

    div[data-baseweb="base-input"] input, textarea {{
        caret-color: {tokens.accent};
    }}

    .stButton > button, .stDownloadButton > button {{
        border-radius: 12px;
        border: 1px solid rgba(14, 165, 233, 0.24);
        background: {tokens.button_bg};
        color: {tokens.button_text};
        font-weight: 650;
        padding: 0.58rem 0.95rem;
        box-shadow: {tokens.shadow};
        transition: transform 0.16s ease, filter 0.16s ease, box-shadow 0.16s ease;
    }}

    .stButton > button:hover, .stDownloadButton > button:hover {{
        filter: brightness(1.02);
        transform: translateY(-1px);
    }}

    .stButton > button:focus-visible, .stDownloadButton > button:focus-visible {{
        outline: 2px solid {tokens.accent};
        outline-offset: 2px;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.4rem;
        background: transparent;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 999px;
        padding: 0.5rem 0.85rem;
        background: {tokens.tab_bg};
        color: {tokens.muted};
        border: 1px solid {tokens.border};
        transition: background-color 0.16s ease, color 0.16s ease, border-color 0.16s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {tokens.text};
        border-color: rgba(14, 165, 233, 0.28);
    }}

    .stTabs [aria-selected="true"] {{
        background: rgba(14, 165, 233, 0.12);
        color: {tokens.text};
        border-color: rgba(14, 165, 233, 0.22);
    }}

    [data-baseweb="popover"], [data-baseweb="menu"], [data-baseweb="listbox"] {{
        background: {tokens.card_bg};
        color: {tokens.text};
        border-color: {tokens.border};
    }}

    [data-testid="stExpander"] {{
        border: 1px solid {tokens.border};
        border-radius: 16px;
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
    }}

    [data-testid="stExpander"] summary {{
        color: {tokens.text};
    }}

    [data-testid="stExpander"] div {{
        color: {tokens.text};
    }}

    .sidebar-card {{
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        border-radius: 18px;
        padding: 0.85rem;
        box-shadow: {tokens.shadow};
    }}

    .section-head {{
        display: grid;
        gap: 0.24rem;
        margin: 0.2rem 0 0.7rem 0;
    }}

    .section-head__eyebrow {{
        color: {tokens.accent};
        font-size: 0.7rem;
        font-weight: 650;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }}

    .section-head__title {{
        color: {tokens.text};
        font-size: 1rem;
        font-weight: 700;
        line-height: 1.2;
    }}

    .section-head__text {{
        color: {tokens.muted};
        font-size: 0.89rem;
        line-height: 1.5;
        max-width: 70ch;
    }}

    .empty-state {{
        border: 1px solid {tokens.border};
        background: {tokens.card_bg};
        border-radius: 20px;
        box-shadow: {tokens.shadow};
        padding: 1rem 1.05rem;
        margin-top: 0.7rem;
    }}

    .empty-state__title {{
        color: {tokens.text};
        font-size: 0.98rem;
        font-weight: 700;
        margin: 0;
    }}

    .empty-state__text {{
        color: {tokens.muted};
        margin: 0.35rem 0 0 0;
        line-height: 1.5;
        font-size: 0.9rem;
    }}

    .empty-state__steps {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.95rem;
    }}

    .topstrip {{
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 0.75rem;
        align-items: center;
        padding: 0.85rem 1rem;
        border: 1px solid {tokens.border};
        border-radius: 18px;
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        margin: 0.2rem 0 0.9rem 0;
    }}

    .topstrip__title {{
        color: {tokens.text};
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0;
    }}

    .topstrip__text {{
        color: {tokens.muted};
        margin: 0.2rem 0 0 0;
        font-size: 0.88rem;
        line-height: 1.45;
    }}

    .topstrip__chips {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        justify-content: flex-end;
    }}

    .decision-card {{
        display: grid;
        gap: 0.35rem;
        border: 1px solid {tokens.border};
        border-radius: 18px;
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        padding: 0.95rem 1rem;
    }}

    .decision-card__label {{
        color: {tokens.muted};
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.13em;
    }}

    .decision-card__value {{
        color: {tokens.text};
        font-size: 1.15rem;
        font-weight: 750;
        letter-spacing: -0.02em;
    }}

    .decision-card__text {{
        color: {tokens.muted};
        font-size: 0.9rem;
        line-height: 1.5;
    }}

    .process-row {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.75rem;
        margin-top: 0.8rem;
    }}

    .process-step {{
        border: 1px solid {tokens.border};
        border-radius: 18px;
        background: {tokens.card_bg};
        box-shadow: {tokens.shadow};
        padding: 0.9rem 0.95rem;
    }}

    .process-step__label {{
        color: {tokens.accent};
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }}

    .process-step__title {{
        color: {tokens.text};
        margin-top: 0.35rem;
        font-size: 0.95rem;
        font-weight: 700;
    }}

    .process-step__text {{
        color: {tokens.muted};
        margin-top: 0.25rem;
        font-size: 0.88rem;
        line-height: 1.45;
    }}

    .stProgress > div > div > div {{
        background: {tokens.button_bg};
    }}

    hr {{
        border-color: {tokens.border};
        opacity: 0.8;
    }}

    @media (max-width: 960px) {{
        .feature-grid, .kpi-grid, .report-grid {{
            grid-template-columns: 1fr;
        }}

        main .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
    }}
</style>
"""
