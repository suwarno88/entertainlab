"""Halaman utama: hero banner, ringkasan tiga platform, dan panduan belajar."""

import streamlit as st
from utils.styling import (
    render_concept_card,
    render_highlight,
    render_metric_card,
    render_success,
)


def render():
    # Hero banner
    st.markdown(
        """
        <div class="hero-banner">
            <h1>🤖 AI Entertainment Lab</h1>
            <p>
                Eksplorasi interaktif bagaimana <strong>Netflix</strong>, <strong>Spotify</strong>,
                dan <strong>YouTube</strong> menggunakan kecerdasan buatan untuk memahami selera Anda
                dan merekomendasikan konten yang paling relevan — dari user-item matrix sampai
                neural network ranking. Dirancang khusus untuk mahasiswa PGSD agar mudah dipahami.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Ringkasan tiga platform
    st.markdown("### 📚 Tiga Studi Kasus Utama")
    st.write("Pilih modul di sidebar untuk memulai simulasi interaktif:")

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        render_concept_card(
            "🎬",
            "Netflix",
            "Bagaimana Netflix merekomendasikan film/serial berdasarkan riwayat tontonan Anda? "
            "Pelajari <em>Collaborative Filtering</em> dan <em>Content-Based Filtering</em> "
            "melalui simulasi user-item matrix dan cosine similarity.",
        )
    with c2:
        render_concept_card(
            "🎵",
            "Spotify",
            "Bagaimana Spotify menemukan lagu yang \"pas\" dengan mood Anda? "
            "Eksplorasi <em>audio features</em> seperti danceability, energy, dan valence, "
            "lalu lihat bagaimana AI mencari lagu serupa di katalog.",
        )
    with c3:
        render_concept_card(
            "▶️",
            "YouTube",
            "Bagaimana YouTube memilih video berikutnya untuk Anda? "
            "Pahami pipeline dua tahap <em>candidate generation</em> dan <em>ranking</em> "
            "dengan berbagai sinyal engagement.",
        )

    st.markdown("---")

    # Statistik tambahan
    st.markdown("### 📊 Skala Industri AI Hiburan")
    st.caption("Estimasi data publik untuk gambaran besarnya tantangan rekomendasi:")

    m1, m2, m3, m4 = st.columns(4, gap="small")
    with m1:
        render_metric_card("Pengguna Netflix", "260+ juta")
    with m2:
        render_metric_card("Lagu di Spotify", "100+ juta")
    with m3:
        render_metric_card("Video YouTube/menit", "500+ jam")
    with m4:
        render_metric_card("Akurasi Rekomendasi", "≈ 80%")

    st.markdown("---")

    # Panduan belajar
    st.markdown("### 🗺️ Panduan Belajar Disarankan")
    render_highlight(
        "<strong>💡 Rute belajar yang efektif:</strong> Mulai dari <em>Konsep Dasar AI Rekomendasi</em> "
        "untuk memahami teori, lalu coba ketiga modul simulasi secara berurutan. "
        "Setiap modul memiliki kontrol parameter yang bisa Anda ubah untuk melihat efeknya pada hasil rekomendasi."
    )

    steps = [
        ("1", "Konsep Dasar AI Rekomendasi", "Pelajari prinsip kerja sistem rekomendasi dan tiga pendekatan utamanya."),
        ("2", "Modul Netflix",               "Eksperimen dengan Collaborative Filtering melalui user-item matrix."),
        ("3", "Modul Spotify",               "Atur preferensi audio features dan lihat bagaimana lagu dicarikan."),
        ("4", "Modul YouTube",               "Pahami pipeline ranking dengan multi-signal engagement."),
        ("5", "Tentang & Sumber Kode",       "Lihat kode di GitHub dan pelajari cara meng-deploy sendiri."),
    ]
    for num, title, desc in steps:
        st.markdown(
            f"""
            <div class="concept-card" style="margin-bottom: 0.6rem;">
                <span class="step-badge">{num}</span>
                <strong>{title}</strong><br>
                <span style="opacity: 0.85; font-size: 0.92rem;">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    render_success(
        "🎓 <strong>Untuk Pendidik:</strong> Materi ini dirancang dalam Bahasa Indonesia "
        "dengan analogi sederhana, cocok untuk dijadikan bahan ajar di kelas atau diskusi "
        "kelompok. Semua simulasi berjalan di browser tanpa perlu install apapun."
    )
