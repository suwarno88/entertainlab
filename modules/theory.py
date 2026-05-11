"""Modul Teori: Fondasi sistem rekomendasi AI."""

import streamlit as st
import plotly.graph_objects as go
from utils.styling import (
    plotly_template,
    render_concept_card,
    render_highlight,
    render_warning,
)


def _flowchart_recommendation():
    """Flowchart konseptual proses rekomendasi."""
    fig = go.Figure()

    # Posisi simpul (x, y)
    nodes = [
        ("Data Pengguna",        0.1, 0.7, "#7C9EFF"),
        ("Data Konten",          0.1, 0.3, "#F59E0B"),
        ("Feature Engineering",  0.35, 0.5, "#8B5CF6"),
        ("Model AI",             0.6, 0.5, "#10B981"),
        ("Skor Relevansi",       0.82, 0.7, "#EF4444"),
        ("Top-N Rekomendasi",    0.82, 0.3, "#06B6D4"),
    ]

    # Edges
    edges = [
        (0, 2), (1, 2), (2, 3), (3, 4), (3, 5),
    ]

    for s, e in edges:
        fig.add_trace(go.Scatter(
            x=[nodes[s][1], nodes[e][1]],
            y=[nodes[s][2], nodes[e][2]],
            mode="lines",
            line=dict(color="#9CA3AF", width=2),
            hoverinfo="skip",
            showlegend=False,
        ))

    for name, x, y, color in nodes:
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            marker=dict(size=55, color=color, line=dict(color="white", width=2)),
            text=[name],
            textposition="middle center",
            textfont=dict(size=11, color="white", family="system-ui"),
            hoverinfo="skip",
            showlegend=False,
        ))

    fig.update_layout(
        **plotly_template()["layout"],
        height=350,
        margin=dict(l=10, r=10, t=20, b=20),
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
    )
    return fig


def render():
    st.markdown(
        """
        <div class="hero-banner" style="background: linear-gradient(135deg, #3B5BDB 0%, #8B5CF6 100%);">
            <h1>📖 Konsep Dasar AI Rekomendasi</h1>
            <p>Sebelum mengeksplorasi simulasi Netflix, Spotify, dan YouTube, mari pahami dulu
            bagaimana sistem rekomendasi bekerja secara umum.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # APA ITU SISTEM REKOMENDASI?
    st.markdown("## 🤔 Apa itu Sistem Rekomendasi?")
    st.write(
        "**Sistem rekomendasi** adalah program AI yang memprediksi *seberapa besar kemungkinan* "
        "seorang pengguna menyukai suatu item (film, lagu, video), lalu mengurutkan item-item tersebut "
        "dari yang paling cocok ke yang paling tidak cocok."
    )

    render_highlight(
        "<strong>Analogi sederhana:</strong> Bayangkan seorang penjaga toko buku yang sangat hafal "
        "selera setiap pelanggan. Ketika Anda datang, ia langsung menyarankan buku-buku yang "
        "kemungkinan besar Anda sukai berdasarkan buku-buku yang pernah Anda beli sebelumnya. "
        "Sistem rekomendasi AI melakukan hal yang sama, tetapi untuk <em>jutaan pengguna sekaligus</em>."
    )

    # FLOWCHART
    st.markdown("## 🔄 Alur Kerja Umum Sistem Rekomendasi")
    st.plotly_chart(_flowchart_recommendation(), use_container_width=True, config={"displayModeBar": False})

    with st.expander("📝 Penjelasan setiap tahap (bahasa sederhana)"):
        st.markdown(
            """
            1. **Data Pengguna** — semua jejak digital Anda: film apa yang pernah ditonton,
               video apa yang di-like, lagu apa yang sering diputar, dan sebagainya.
            2. **Data Konten** — informasi tentang item itu sendiri: genre film, durasi video,
               nama artis lagu, tahun rilis, dan ciri lainnya.
            3. **Feature Engineering** (Mengolah Ciri-ciri) — mengubah data mentah (misalnya "genre: Komedi")
               menjadi sekumpulan angka agar bisa dihitung komputer. Bayangkan seperti memberi nilai
               raport untuk setiap film.
            4. **Model AI** — "otak" yang mempelajari pola dari data. Ada beberapa cara: ada yang
               membandingkan selera antar pengguna, ada yang membandingkan ciri antar item,
               atau gabungan keduanya.
            5. **Skor Kecocokan** — model menghasilkan angka 0–1 untuk setiap pasangan (pengguna, item).
               Angka mendekati 1 = sangat cocok; mendekati 0 = tidak cocok.
            6. **Daftar Rekomendasi Teratas** — ambil sejumlah item dengan skor tertinggi,
               tampilkan di beranda Anda.
            """
        )

    st.markdown("---")

    # TIGA PENDEKATAN UTAMA
    st.markdown("## 🎯 Tiga Pendekatan Utama")

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        render_concept_card(
            "👥",
            "Collaborative Filtering",
            "Mencari pengguna lain yang <strong>seleranya mirip</strong> dengan Anda, "
            "lalu merekomendasikan tontonan yang mereka sukai tapi belum Anda coba. "
            "Logikanya: \"Pengguna yang menonton X juga menonton Y.\" "
            "<br><br>Cara ini dipakai Netflix untuk menyarankan serial baru.",
        )
    with c2:
        render_concept_card(
            "🏷️",
            "Content-Based Filtering",
            "Mencari item lain yang <strong>mirip dengan item</strong> yang sudah Anda sukai, "
            "berdasarkan ciri-cirinya (genre, kata kunci, suara, dll). "
            "<br><br>Contoh: Spotify mencari lagu dengan tempo dan tingkat energi serupa dengan "
            "lagu-lagu favorit Anda.",
        )
    with c3:
        render_concept_card(
            "🔀",
            "Hybrid (Gabungan)",
            "Menggabungkan kedua pendekatan di atas, sering ditambah teknik AI canggih "
            "(<em>deep learning</em>) untuk menangkap pola rumit. "
            "<br><br>YouTube menggunakan cara ini lewat dua tahap: memilih video kandidat lalu "
            "merangking ulang berdasarkan banyak sinyal.",
        )

    st.markdown("---")

    # COSINE SIMILARITY
    st.markdown("## 📐 Kunci Matematis: Cosine Similarity")
    st.write(
        "Hampir semua sistem rekomendasi modern menggunakan satu konsep matematika sederhana: "
        "**mengukur kemiripan dua daftar angka**. Cara paling populer disebut **cosine similarity**. "
        "Bayangkan setiap pengguna (atau item) digambarkan sebagai sebuah panah yang menunjuk ke arah "
        "tertentu — semakin sama arahnya, semakin mirip seleranya."
    )

    st.markdown(
        """
        <div class="formula-block">
        Hasilnya berupa angka antara −1 dan +1:<br><br>
        &nbsp;&nbsp;<strong>+1</strong> → arah sama persis (sangat mirip ✅)<br>
        &nbsp;&nbsp;&nbsp;<strong>0</strong> → tegak lurus (tidak ada hubungan)<br>
        &nbsp;&nbsp;<strong>−1</strong> → arah berlawanan (sangat berbeda ❌)
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_highlight(
        "<strong>Analogi sederhana:</strong> Bayangkan Anda dan teman Anda diminta menilai 10 film "
        "dengan skala 1–5. Jika nilai-nilai Anda berdua naik-turun di film yang sama "
        "(suka film A, tidak suka film B), maka cosine similarity Anda berdua mendekati +1 "
        "— alias seleranya mirip. AI memanfaatkan kemiripan ini untuk menebak film apa lagi "
        "yang mungkin Anda sukai."
    )

    # TANTANGAN
    st.markdown("---")
    st.markdown("## ⚠️ Tantangan Umum")

    challenges = [
        ("🥶 Cold Start (Pengguna Baru)",
         "Bagaimana merekomendasikan untuk pengguna yang baru daftar dan belum punya riwayat sama sekali? "
         "Solusinya: bertanya dulu lewat survei singkat saat onboarding, atau pakai data demografis."),
        ("📉 Sparsity (Data Banyak yang Kosong)",
         "Kebanyakan pengguna hanya menonton sebagian kecil dari semua film yang tersedia. Jadi tabelnya "
         "banyak sel kosong. Solusinya: pakai teknik matematika canggih yang bisa 'menebak' angka kosong."),
        ("🔄 Filter Bubble (Terjebak di Selera Sempit)",
         "Kalau sistem hanya merekomendasikan film yang mirip-mirip, pengguna jadi tidak pernah "
         "kenal genre baru. Solusinya: sengaja tambahkan variasi (eksplorasi) di rekomendasi."),
        ("⚡ Skalabilitas (Data Sangat Besar)",
         "Netflix punya 260+ juta pengguna dan jutaan film. Tidak mungkin menghitung kemiripan satu per satu. "
         "Solusinya: pakai teknik pencarian cepat (approximate nearest neighbors) dan ringkasan data (embedding)."),
    ]
    for title, desc in challenges:
        st.markdown(
            f"""
            <div class="concept-card" style="margin-bottom: 0.6rem;">
                <strong>{title}</strong><br>
                <span style="opacity: 0.85; font-size: 0.92rem;">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_warning(
        "<strong>📌 Catatan untuk Pendidik:</strong> Materi ini menyederhanakan kompleksitas teknis "
        "agar mahasiswa PGSD dapat memahami prinsip dasarnya. Implementasi nyata di industri "
        "melibatkan deep learning, embedding, distributed computing, dan A/B testing skala besar."
    )
