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

    with st.expander("📝 Penjelasan setiap tahap"):
        st.markdown(
            """
            1. **Data Pengguna** — riwayat tontonan, rating, klik, durasi menonton, like/dislike.
            2. **Data Konten** — informasi item: genre, durasi, tahun, fitur audio/visual.
            3. **Feature Engineering** — mengubah data mentah menjadi representasi numerik (vektor)
               yang bisa diolah model.
            4. **Model AI** — algoritma yang mempelajari pola: Collaborative Filtering, Content-Based,
               Deep Neural Network, atau gabungan (Hybrid).
            5. **Skor Relevansi** — model menghasilkan angka 0–1 untuk setiap pasangan (pengguna, item).
            6. **Top-N Rekomendasi** — ambil N item dengan skor tertinggi untuk ditampilkan.
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
            "lalu merekomendasikan item yang mereka sukai tetapi belum Anda coba. "
            "Contoh: \"Pengguna yang menonton X juga menonton Y.\" Digunakan oleh Netflix.",
        )
    with c2:
        render_concept_card(
            "🏷️",
            "Content-Based Filtering",
            "Mencari item yang <strong>mirip dengan item</strong> yang sudah Anda sukai, "
            "berdasarkan ciri-ciri konten (genre, kata kunci, fitur audio). "
            "Contoh: Spotify mencari lagu dengan tempo dan energy serupa.",
        )
    with c3:
        render_concept_card(
            "🔀",
            "Hybrid (Gabungan)",
            "Menggabungkan dua pendekatan di atas, sering ditambah <strong>deep learning</strong> "
            "untuk menangkap pola kompleks. Digunakan YouTube dengan pipeline "
            "<em>candidate generation</em> + <em>ranking</em>.",
        )

    st.markdown("---")

    # COSINE SIMILARITY
    st.markdown("## 📐 Kunci Matematis: Cosine Similarity")
    st.write(
        "Hampir semua sistem rekomendasi modern menggunakan konsep **kemiripan vektor**. "
        "Cara paling umum adalah **cosine similarity** — yaitu mengukur seberapa sejajar "
        "arah dua vektor di ruang multi-dimensi."
    )

    st.markdown(
        """
        <div class="formula-block">
        cos(θ) = (A · B) / (||A|| × ||B||)<br><br>
        Hasil:<br>
        &nbsp;&nbsp;<strong>+1</strong> → arah sama persis (sangat mirip)<br>
        &nbsp;&nbsp;&nbsp;<strong>0</strong> → tegak lurus (tidak ada hubungan)<br>
        &nbsp;&nbsp;<strong>−1</strong> → arah berlawanan (sangat berbeda)
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_highlight(
        "<strong>Intuisi sederhana:</strong> Bayangkan setiap pengguna direpresentasikan oleh sebuah "
        "panah di ruang multi-dimensi (di mana setiap dimensi adalah satu item yang sudah dirating). "
        "Dua pengguna dengan selera mirip akan memiliki panah yang menunjuk ke arah yang sama. "
        "Cosine similarity mengukur seberapa sejajar kedua panah tersebut."
    )

    # TANTANGAN
    st.markdown("---")
    st.markdown("## ⚠️ Tantangan Umum")

    challenges = [
        ("🥶 Cold Start", "Bagaimana merekomendasikan untuk pengguna baru yang belum punya riwayat? Solusi: gunakan data demografis atau onboarding survey."),
        ("📉 Sparsity",   "Kebanyakan pengguna hanya berinteraksi dengan sebagian kecil item. Matrix-nya jadi banyak kosong. Solusi: matrix factorization, deep learning."),
        ("🔄 Filter Bubble", "Jika hanya merekomendasikan yang mirip, pengguna terjebak di selera sempit. Solusi: tambahkan faktor diversitas dan eksplorasi."),
        ("⚡ Skalabilitas", "Netflix punya 260+ juta pengguna × jutaan item. Komputasi cosine similarity langsung tidak feasible. Solusi: approximate nearest neighbors, embedding."),
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
