"""Halaman Tentang: dokumentasi, instruksi penggunaan, dan link GitHub."""

import streamlit as st
from utils.styling import render_concept_card, render_highlight, render_success, render_warning


def render():
    st.markdown(
        """
        <div class="hero-banner" style="background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);">
            <h1>📚 Tentang & Dokumentasi</h1>
            <p>Panduan lengkap penggunaan AI Entertainment Lab dan referensi untuk eksplorasi lebih lanjut.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- TUJUAN ----------
    st.markdown("## 🎯 Tujuan Pembelajaran")
    st.write(
        "Setelah menggunakan AI Entertainment Lab, mahasiswa diharapkan dapat:"
    )
    objectives = [
        "Menjelaskan prinsip kerja sistem rekomendasi AI dalam bahasa sederhana.",
        "Membedakan tiga pendekatan utama: Collaborative Filtering, Content-Based, dan Hybrid.",
        "Mengidentifikasi sinyal-sinyal yang digunakan oleh Netflix, Spotify, dan YouTube.",
        "Memahami konsep cosine similarity sebagai dasar matematis sistem rekomendasi.",
        "Mengaitkan teknologi AI rekomendasi dengan pengalaman sehari-hari di dunia digital.",
    ]
    for o in objectives:
        st.markdown(f"- {o}")

    st.markdown("---")

    # ---------- CARA PAKAI ----------
    st.markdown("## 📖 Cara Menggunakan Simulasi")

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        render_concept_card(
            "1️⃣",
            "Mulai dari Teori",
            "Buka modul <strong>Konsep Dasar AI Rekomendasi</strong> di sidebar untuk memahami "
            "fondasi teori sebelum bereksperimen.",
        )
        render_concept_card(
            "3️⃣",
            "Ubah Parameter",
            "Setiap simulasi memiliki slider dan dropdown. Ubah satu parameter pada satu waktu, "
            "lalu amati bagaimana hasil rekomendasi berubah.",
        )
    with c2:
        render_concept_card(
            "2️⃣",
            "Pilih Studi Kasus",
            "Pilih Netflix, Spotify, atau YouTube dari sidebar. Setiap modul fokus pada "
            "satu pendekatan utama agar tidak overwhelming.",
        )
        render_concept_card(
            "4️⃣",
            "Baca Insight",
            "Setiap modul diakhiri dengan kotak \"Pelajaran kunci\" — bagian penting yang "
            "merangkum apa yang baru saja Anda eksperimenkan.",
        )

    render_highlight(
        "🎓 <strong>Tips untuk Dosen/Guru:</strong> Berikan tugas eksplorasi terstruktur: "
        "minta mahasiswa membandingkan hasil dengan parameter ekstrem (misal k=2 vs k=6 di Netflix), "
        "lalu menulis refleksi singkat tentang trade-off-nya. Ini melatih critical thinking."
    )

    st.markdown("---")

    # ---------- SUMBER KODE ----------
    st.markdown("## 💻 Sumber Kode & Deployment")

    st.write(
        "Project ini bersifat **open source** dan dapat di-deploy oleh siapa saja menggunakan "
        "GitHub + Streamlit Community Cloud (gratis)."
    )

    st.markdown("### 🔧 Struktur Project")
    st.code(
        """ai-entertainment-lab/
├── streamlit_app.py          # Entry point utama
├── requirements.txt          # Dependencies
├── README.md                 # Dokumentasi
├── .streamlit/
│   └── config.toml           # Default theme
├── modules/                  # Modul halaman (BUKAN 'pages/' agar tidak konflik)
│   ├── home.py
│   ├── theory.py
│   ├── netflix.py
│   ├── spotify.py
│   ├── youtube.py
│   └── about.py
└── utils/                    # Utilitas
    ├── styling.py            # CSS injection (dark/light mode)
    └── data.py               # Dataset sintetis
""",
        language="text",
    )

    st.markdown("### 🚀 Cara Deploy ke Streamlit Cloud")
    steps = [
        ("1.", "Buat repository baru di **GitHub** dan unggah semua file project."),
        ("2.", "Login ke [share.streamlit.io](https://share.streamlit.io) menggunakan akun GitHub."),
        ("3.", "Klik **\"New app\"**, pilih repository dan branch."),
        ("4.", "Set **Main file path** ke `streamlit_app.py`."),
        ("5.", "Klik **Deploy**. Streamlit akan otomatis install dependencies dari `requirements.txt`."),
    ]
    for num, desc in steps:
        st.markdown(f"**{num}** {desc}")

    render_warning(
        "📌 <strong>Catatan penting:</strong> Jangan pernah menamai folder modul sebagai "
        "<code>pages/</code> — Streamlit Cloud akan otomatis menafsirkannya sebagai native "
        "multipage app dan navigation sidebar akan kosong. Gunakan nama lain seperti "
        "<code>modules/</code> dan handle routing manual seperti yang dilakukan di project ini."
    )

    st.markdown("### 💻 Menjalankan di Lokal")
    st.code(
        """# Clone repo
git clone https://github.com/USERNAME/ai-entertainment-lab.git
cd ai-entertainment-lab

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run streamlit_app.py""",
        language="bash",
    )

    st.markdown("---")

    # ---------- TEKNOLOGI ----------
    st.markdown("## 🛠️ Teknologi yang Digunakan")
    tech = [
        ("🐍 Python 3.10+",         "Bahasa utama untuk logika rekomendasi"),
        ("⚡ Streamlit",             "Framework untuk web app berbasis Python"),
        ("📊 Plotly",                "Visualisasi interaktif (heatmap, scatter, radar)"),
        ("🔢 NumPy & Pandas",        "Manipulasi data dan komputasi vektor"),
        ("🤖 scikit-learn",          "Utilitas untuk cosine similarity & preprocessing"),
    ]
    for icon_name, desc in tech:
        st.markdown(f"- **{icon_name}** — {desc}")

    st.markdown("---")

    # ---------- REFERENSI ----------
    st.markdown("## 📚 Referensi Lanjutan")
    refs = [
        "Gomez-Uribe, C. A. & Hunt, N. (2016). *The Netflix Recommender System: Algorithms, Business Value, and Innovation.* ACM Transactions on Management Information Systems.",
        "Covington, P., Adams, J., & Sargin, E. (2016). *Deep Neural Networks for YouTube Recommendations.* RecSys 2016. — Paper resmi YouTube tentang two-stage pipeline.",
        "Spotify Engineering Blog: *Discover Weekly: How We Build Personalized Playlists.* — Penjelasan publik tentang collaborative filtering Spotify.",
        "Aggarwal, C. C. (2016). *Recommender Systems: The Textbook.* Springer. — Referensi komprehensif untuk pembelajaran lebih dalam.",
        "Ricci, F., Rokach, L., & Shapira, B. (Eds.). (2022). *Recommender Systems Handbook* (3rd ed.). Springer.",
    ]
    for r in refs:
        st.markdown(f"- {r}")

    st.markdown("---")

    # ---------- KREDIT ----------
    render_success(
        "🙏 <strong>Kredit:</strong> Materi ini dirancang sebagai bahan ajar untuk mata kuliah "
        "<em>Fondasi Kecerdasan Buatan</em> di program PGSD. Dataset bersifat sintetis dan dibuat "
        "untuk tujuan edukasi semata — tidak merepresentasikan data nyata dari Netflix, Spotify, "
        "atau YouTube."
    )
