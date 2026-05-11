# 🤖 AI Entertainment Lab

> **Materi Edukasi Interaktif** — Eksplorasi bagaimana Netflix, Spotify, dan YouTube menggunakan AI untuk merekomendasikan konten kepada Anda.

Aplikasi web Streamlit yang dirancang sebagai bahan ajar mata kuliah **Fondasi Kecerdasan Buatan** di program PGSD. Cocok untuk mahasiswa dan pengajar dengan latar belakang non-teknis.

---

## ✨ Fitur Utama

- 🎬 **Simulasi Netflix** — Collaborative Filtering, Content-Based, dan Hybrid dengan user-item matrix interaktif
- 🎵 **Simulasi Spotify** — Audio features dengan mood profile slider (Danceability, Energy, Valence, dll.)
- ▶️ **Simulasi YouTube** — Two-stage pipeline (Candidate Generation + Multi-Signal Ranking)
- 📖 **Modul Teori** — Penjelasan konsep dasar dengan flowchart dan analogi sederhana
- 🌗 **Dark & Light Mode** — Toggle di sidebar untuk kenyamanan visual
- 🇮🇩 **Konten Berbahasa Indonesia** — Disesuaikan untuk mahasiswa PGSD
- 📊 **Visualisasi Plotly** — Heatmap, radar chart, scatter plot, stacked bar, flowchart

---

## 🎯 Tujuan Pembelajaran

Setelah menggunakan aplikasi ini, mahasiswa diharapkan dapat:

1. Menjelaskan prinsip kerja sistem rekomendasi AI dalam bahasa sederhana.
2. Membedakan tiga pendekatan utama: Collaborative Filtering, Content-Based, dan Hybrid.
3. Mengidentifikasi sinyal-sinyal yang digunakan Netflix, Spotify, dan YouTube.
4. Memahami konsep cosine similarity sebagai dasar matematis sistem rekomendasi.
5. Mengaitkan teknologi AI dengan pengalaman sehari-hari di dunia digital.

---

## 🚀 Quick Start

### Menjalankan di Lokal

```bash
# Clone repository
git clone https://github.com/USERNAME/ai-entertainment-lab.git
cd ai-entertainment-lab

# (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
# atau
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run streamlit_app.py
```

Buka browser di `http://localhost:8501`.

### Deploy ke Streamlit Community Cloud (Gratis)

1. **Upload ke GitHub** — buat repository baru, push semua file project.
2. **Login** ke [share.streamlit.io](https://share.streamlit.io) menggunakan akun GitHub.
3. **New app** — pilih repository, branch (`main`), dan main file (`streamlit_app.py`).
4. **Deploy** — tunggu 1-3 menit, aplikasi langsung online dengan URL publik.

---

## 📁 Struktur Project

```
ai-entertainment-lab/
├── streamlit_app.py          # Entry point utama (routing manual)
├── requirements.txt          # Python dependencies
├── README.md                 # Dokumentasi ini
├── .streamlit/
│   └── config.toml           # Default theme config
├── modules/                  # ⚠️ BUKAN 'pages/' — hindari konflik native multipage
│   ├── __init__.py
│   ├── home.py               # Dashboard utama
│   ├── theory.py             # Modul teori dasar
│   ├── netflix.py            # Simulasi Netflix
│   ├── spotify.py            # Simulasi Spotify
│   ├── youtube.py            # Simulasi YouTube
│   └── about.py              # Halaman tentang & dokumentasi
└── utils/
    ├── __init__.py
    ├── styling.py            # CSS injection (dark/light mode)
    └── data.py               # Generator dataset sintetis
```

### ⚠️ Catatan Penting: Hindari Folder `pages/`

Streamlit Cloud otomatis menafsirkan folder bernama `pages/` sebagai *native multipage app*, yang akan membuat navigation sidebar custom **kosong**. Project ini menamai folder modul sebagai `modules/` dan menangani routing manual di `streamlit_app.py`.

---

## 🛠️ Teknologi

| Komponen | Library | Fungsi |
|----------|---------|--------|
| Web framework | Streamlit | UI interaktif berbasis Python |
| Visualisasi | Plotly | Chart interaktif (heatmap, radar, scatter, stacked bar) |
| Komputasi | NumPy, Pandas | Operasi matriks & dataframe |
| ML utilities | scikit-learn | Cosine similarity, normalisasi |

---

## 📚 Daftar Modul Detail

### 1. 🏠 Beranda
Dashboard utama dengan hero banner, ringkasan ketiga platform, metrik skala industri, dan panduan rute belajar.

### 2. 📖 Konsep Dasar AI Rekomendasi
- Definisi sistem rekomendasi dengan analogi penjaga toko buku.
- Flowchart umum proses rekomendasi.
- Tiga pendekatan utama: Collaborative Filtering, Content-Based, Hybrid.
- Penjelasan cosine similarity dengan formula dan intuisi geometris.
- Tantangan klasik: cold start, sparsity, filter bubble, skalabilitas.

### 3. 🎬 Netflix — Personalization
**Interaktivitas:**
- Pilih salah satu dari 8 pengguna sintetis (masing-masing punya preferensi genre berbeda).
- Toggle algoritma: Collaborative Filtering / Content-Based / Hybrid.
- Slider jumlah neighbor (k=2..6).
- Slider bobot CF vs CB (untuk mode Hybrid).

**Visualisasi:**
- Heatmap user-item matrix (8 user × 20 film) dengan baris target di-highlight.
- Bar chart cosine similarity antar user, top-k di-highlight merah.
- Bar chart Top-N rekomendasi.
- Tabel detail skor dengan breakdown.

### 4. 🎵 Spotify — Music Discovery
**Interaktivitas:**
- 4 preset mood (Workout, Chill, Party, Belajar) atau slider manual.
- 6 audio feature sliders (Danceability, Energy, Valence, Acousticness, Tempo, Instrumentalness).
- Multi-select filter genre.
- Slider faktor eksplorasi (eksploitasi ↔ discovery).

**Visualisasi:**
- Radar chart profil user vs rerata katalog.
- Top-8 rekomendasi dengan similarity score.
- Scatter plot 2D katalog lagu (sumbu X & Y dipilih user).

### 5. ▶️ YouTube — Video Recommendations
**Interaktivitas:**
- Multi-select kategori minat (filter Tahap 1).
- Slider minimum watch completion.
- 5 slider bobot sinyal: Watch Completion, CTR, Like Ratio, Freshness, Popularity.

**Visualisasi:**
- Flowchart pipeline dua tahap.
- Scatter plot kandidat (lolos filter vs tidak).
- Stacked bar chart kontribusi tiap sinyal pada skor akhir.
- Tabel Top-10 dengan background gradient.

### 6. ℹ️ Tentang & Dokumentasi
- Tujuan pembelajaran terstruktur.
- Panduan langkah-demi-langkah menggunakan simulasi.
- Instruksi deployment ke Streamlit Cloud.
- Referensi akademik lanjutan.

---

## 🎓 Untuk Pendidik

### Saran Penggunaan di Kelas

1. **Sesi 1 — Pengantar (30 menit)** — Buka modul Teori bersama, diskusikan analogi.
2. **Sesi 2 — Netflix (45 menit)** — Eksplorasi user-item matrix, tugas: bandingkan rekomendasi untuk 3 pengguna berbeda.
3. **Sesi 3 — Spotify (45 menit)** — Setiap kelompok memilih mood profile, presentasikan lagu yang muncul.
4. **Sesi 4 — YouTube (45 menit)** — Diskusi: mengapa YouTube butuh banyak sinyal? Eksperimen dengan extreme weights.
5. **Sesi 5 — Refleksi (30 menit)** — Diskusi etika: filter bubble, algoritma bias, privasi.

### Pertanyaan Pemantik Diskusi

- "Apa risiko jika YouTube hanya pakai sinyal 'watch time'?" → mendiskusikan clickbait.
- "Bagaimana Spotify merekomendasikan untuk pengguna baru?" → cold start problem.
- "Apakah baik jika semua rekomendasi selalu mirip dengan yang pernah kita tonton?" → filter bubble.

---

## 📖 Referensi Akademik

- Gomez-Uribe, C. A. & Hunt, N. (2016). *The Netflix Recommender System: Algorithms, Business Value, and Innovation.* ACM TMIS.
- Covington, P., Adams, J., & Sargin, E. (2016). *Deep Neural Networks for YouTube Recommendations.* RecSys 2016.
- Aggarwal, C. C. (2016). *Recommender Systems: The Textbook.* Springer.
- Ricci, F., Rokach, L., & Shapira, B. (Eds.). (2022). *Recommender Systems Handbook* (3rd ed.). Springer.

---

## ⚠️ Disclaimer

Dataset di aplikasi ini bersifat **sintetis** dan dibuat khusus untuk tujuan edukasi. Tidak mewakili data nyata dari Netflix, Spotify, atau YouTube. Algoritma yang disimulasikan adalah **versi sederhana** dari yang digunakan platform tersebut di produksi — implementasi nyata melibatkan deep learning skala besar yang berada di luar cakupan pengantar ini.

---

## 📝 Lisensi

MIT License — bebas digunakan, dimodifikasi, dan didistribusikan untuk tujuan edukasi maupun komersial.

---

## 🙏 Kredit

Dibangun dengan ❤️ untuk mahasiswa PGSD BINUS University.
Materi disusun oleh pengampu mata kuliah **Fondasi Kecerdasan Buatan**.
