"""
Styling utilities untuk AI Entertainment Lab.

Mengikuti prinsip:
- Hanya styling custom HTML components (.concept-card, .highlight-box, dll)
- Streamlit native widgets dibiarkan default agar tidak konflik
- Dark & Light mode di-handle via CSS variables yang di-swap berdasarkan session_state
"""

import streamlit as st


# ---------- TEMA WARNA ----------

DARK_THEME = {
    "bg_primary": "#0E1117",
    "bg_secondary": "#1A1D24",
    "bg_card": "#161A22",
    "border": "#2A2F3A",
    "text_primary": "#FAFAFA",
    "text_secondary": "#B8BCC8",
    "accent_netflix": "#E50914",
    "accent_spotify": "#1DB954",
    "accent_youtube": "#FF0000",
    "accent_primary": "#7C9EFF",
    "highlight_bg": "rgba(124, 158, 255, 0.08)",
    "warning_bg": "rgba(255, 193, 7, 0.10)",
    "success_bg": "rgba(29, 185, 84, 0.10)",
    "shadow": "0 4px 20px rgba(0, 0, 0, 0.35)",
}

LIGHT_THEME = {
    "bg_primary": "#FAFAFA",
    "bg_secondary": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "border": "#E5E7EB",
    "text_primary": "#111827",
    "text_secondary": "#4B5563",
    "accent_netflix": "#E50914",
    "accent_spotify": "#1DB954",
    "accent_youtube": "#FF0000",
    "accent_primary": "#3B5BDB",
    "highlight_bg": "rgba(59, 91, 219, 0.06)",
    "warning_bg": "rgba(217, 119, 6, 0.08)",
    "success_bg": "rgba(29, 185, 84, 0.08)",
    "shadow": "0 2px 12px rgba(0, 0, 0, 0.08)",
}


def get_theme():
    """Ambil tema aktif dari session_state."""
    mode = st.session_state.get("theme_mode", "dark")
    return DARK_THEME if mode == "dark" else LIGHT_THEME


def inject_css():
    """
    Inject CSS scoped HANYA untuk custom HTML components.
    Streamlit native widgets dibiarkan default untuk hindari konflik rendering.
    """
    t = get_theme()
    css = f"""
    <style>
    /* ========== CUSTOM COMPONENTS ONLY ========== */

    /* Streamlit column containers — buat anaknya stretch ke tinggi yang sama.
       Ini krusial agar .concept-card height:100% benar-benar bekerja. */
    div[data-testid="stHorizontalBlock"] {{
        align-items: stretch !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{
        display: flex !important;
        flex-direction: column !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div {{
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
    }}

    .hero-banner {{
        background: linear-gradient(135deg, {t['accent_netflix']} 0%, {t['accent_youtube']} 50%, {t['accent_spotify']} 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: #FFFFFF;
        margin-bottom: 1.5rem;
        box-shadow: {t['shadow']};
        position: relative;
        overflow: hidden;
    }}
    .hero-banner h1 {{
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.5px;
    }}
    .hero-banner p {{
        font-size: 1.05rem;
        opacity: 0.95;
        margin: 0;
        max-width: 720px;
    }}

    .concept-card {{
        background: {t['bg_card']};
        border: 1px solid {t['border']};
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
        height: 100%;
        box-sizing: border-box;
        box-shadow: {t['shadow']};
        transition: transform 0.18s ease, border-color 0.18s ease;
    }}
    .concept-card:hover {{
        transform: translateY(-2px);
        border-color: {t['accent_primary']};
    }}
    .concept-card h3 {{
        color: {t['text_primary']};
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }}
    .concept-card p {{
        color: {t['text_secondary']};
        font-size: 0.92rem;
        line-height: 1.55;
        margin: 0;
    }}
    .concept-card .icon-badge {{
        font-size: 1.6rem;
        margin-bottom: 0.5rem;
        display: block;
    }}

    .highlight-box {{
        background: {t['highlight_bg']};
        border-left: 4px solid {t['accent_primary']};
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: {t['text_primary']};
    }}
    .highlight-box strong {{
        color: {t['accent_primary']};
    }}

    .warning-box {{
        background: {t['warning_bg']};
        border-left: 4px solid #F59E0B;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: {t['text_primary']};
    }}

    .success-box {{
        background: {t['success_bg']};
        border-left: 4px solid {t['accent_spotify']};
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: {t['text_primary']};
    }}

    .metric-card {{
        background: {t['bg_card']};
        border: 1px solid {t['border']};
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        height: 100%;
        box-sizing: border-box;
    }}
    .metric-card .label {{
        color: {t['text_secondary']};
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }}
    .metric-card .value {{
        color: {t['text_primary']};
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
    }}

    .step-badge {{
        display: inline-block;
        background: {t['accent_primary']};
        color: #FFFFFF;
        width: 28px;
        height: 28px;
        line-height: 28px;
        text-align: center;
        border-radius: 50%;
        font-weight: 700;
        font-size: 0.85rem;
        margin-right: 0.5rem;
    }}

    .platform-pill {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }}
    .pill-netflix {{ background: {t['accent_netflix']}; color: white; }}
    .pill-spotify {{ background: {t['accent_spotify']}; color: white; }}
    .pill-youtube {{ background: {t['accent_youtube']}; color: white; }}

    .tooltip-text {{
        border-bottom: 1px dotted {t['accent_primary']};
        cursor: help;
        color: {t['accent_primary']};
    }}

    .footer-credit {{
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: {t['text_secondary']};
        font-size: 0.85rem;
        border-top: 1px solid {t['border']};
        margin-top: 2rem;
    }}

    .module-header {{
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }}
    .module-header-netflix {{
        background: linear-gradient(120deg, #831010 0%, {t['accent_netflix']} 100%);
    }}
    .module-header-spotify {{
        background: linear-gradient(120deg, #0d6b30 0%, {t['accent_spotify']} 100%);
    }}
    .module-header-youtube {{
        background: linear-gradient(120deg, #8b0000 0%, {t['accent_youtube']} 100%);
    }}
    .module-header h2 {{
        margin: 0;
        font-size: 1.6rem;
        font-weight: 800;
    }}
    .module-header p {{
        margin: 0.2rem 0 0 0;
        opacity: 0.92;
        font-size: 0.95rem;
    }}

    .formula-block {{
        background: {t['bg_card']};
        border: 1px solid {t['border']};
        border-radius: 8px;
        padding: 1rem 1.2rem;
        font-family: 'Courier New', monospace;
        color: {t['text_primary']};
        margin: 0.8rem 0;
        overflow-x: auto;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def theme_toggle_widget():
    """Toggle dark/light mode di sidebar."""
    current = st.session_state.get("theme_mode", "dark")
    label = "☀️ Light Mode" if current == "dark" else "🌙 Dark Mode"
    if st.sidebar.button(label, use_container_width=True, key="theme_toggle_btn"):
        st.session_state["theme_mode"] = "light" if current == "dark" else "dark"
        st.rerun()


# ---------- KOMPONEN HTML HELPERS ----------

def render_concept_card(icon, title, body):
    """Render concept card dengan icon, title, dan body."""
    st.markdown(
        f"""
        <div class="concept-card">
            <span class="icon-badge">{icon}</span>
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_highlight(text):
    st.markdown(f'<div class="highlight-box">{text}</div>', unsafe_allow_html=True)


def render_warning(text):
    st.markdown(f'<div class="warning-box">{text}</div>', unsafe_allow_html=True)


def render_success(text):
    st.markdown(f'<div class="success-box">{text}</div>', unsafe_allow_html=True)


def render_module_header(platform, title, subtitle):
    """platform: 'netflix' | 'spotify' | 'youtube'"""
    icons = {"netflix": "🎬", "spotify": "🎵", "youtube": "▶️"}
    st.markdown(
        f"""
        <div class="module-header module-header-{platform}">
            <div style="font-size: 2.5rem;">{icons.get(platform, '🤖')}</div>
            <div>
                <h2>{title}</h2>
                <p>{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="footer-credit">
            <strong>AI Entertainment Lab</strong> — Materi Edukasi PGSD: Fondasi Kecerdasan Buatan<br>
            Dibangun dengan ❤️ menggunakan Streamlit • Visualisasi: Plotly
        </div>
        """,
        unsafe_allow_html=True,
    )


def plotly_layout():
    """
    Layout Plotly dasar (tanpa xaxis/yaxis) yang aman di-spread ke fig.update_layout(**...).
    Untuk styling axes, gunakan apply_axes_theme(fig) terpisah setelahnya.
    """
    t = get_theme()
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": t["text_primary"], "family": "system-ui, sans-serif"},
        "colorway": [
            t["accent_primary"], t["accent_netflix"], t["accent_spotify"],
            t["accent_youtube"], "#F59E0B", "#8B5CF6",
        ],
    }


def apply_axes_theme(fig):
    """
    Apply gridcolor & zerolinecolor ke axes existing fig.
    Aman dipanggil meski tidak ada axes (no-op untuk polar/scene).
    """
    t = get_theme()
    fig.update_xaxes(gridcolor=t["border"], zerolinecolor=t["border"])
    fig.update_yaxes(gridcolor=t["border"], zerolinecolor=t["border"])
    return fig


# Backward-compat: tetap sediakan plotly_template() yang mengembalikan dict
# berisi key 'layout' (tanpa xaxis/yaxis) untuk callsite lama.
def plotly_template():
    return {"layout": plotly_layout()}
