"""
AI Entertainment Lab — Entry point utama.

Materi edukasi interaktif tentang AI di industri hiburan untuk PGSD.
Tiga studi kasus utama: Netflix, Spotify, YouTube.

Routing manual digunakan (bukan Streamlit native multipage) agar tidak konflik
dengan folder `modules/` saat di-deploy ke Streamlit Cloud.
"""

import streamlit as st

# ---------- KONFIGURASI HALAMAN ----------
st.set_page_config(
    page_title="AI Entertainment Lab",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inisialisasi session state
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "dark"
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Beranda"

from utils.styling import inject_css, theme_toggle_widget, render_footer
from modules import home, theory, netflix, spotify, youtube, about

# Inject CSS sesuai tema aktif
inject_css()


# ---------- SIDEBAR NAVIGASI ----------
with st.sidebar:
    st.markdown("# 🤖 AI Entertainment Lab")

    st.markdown("---")
    st.markdown("### 📚 Navigasi")

    pages = {
        "🏠 Beranda":                      home.render,
        "📖 Konsep Dasar AI Rekomendasi":  theory.render,
        "🎬 Netflix":                       netflix.render,
        "🎵 Spotify":                       spotify.render,
        "▶️ YouTube":                       youtube.render,
        "ℹ️ Tentang & Dokumentasi":        about.render,
    }

    selected = st.radio(
        "Pilih halaman:",
        options=list(pages.keys()),
        index=list(pages.keys()).index(st.session_state["current_page"])
            if st.session_state["current_page"] in pages else 0,
        label_visibility="collapsed",
    )
    st.session_state["current_page"] = selected

    st.markdown("---")
    st.markdown("### 🎨 Tampilan")
    theme_toggle_widget()

    st.markdown("---")
    st.caption("v1.0 • 2026")


# ---------- RENDER HALAMAN AKTIF ----------
pages[selected]()

# ---------- FOOTER ----------
render_footer()
