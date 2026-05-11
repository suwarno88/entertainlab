"""
Modul Simulasi Spotify: Audio Features & Content-Based Recommendation.

Pengguna bisa:
- Mengatur 'mood profile' via slider (danceability, energy, valence, dll)
- Memilih genre preferensi
- Mengatur balance eksplorasi vs eksploitasi
- Melihat radar chart mood profile
- Mendapat rekomendasi lagu dengan breakdown fitur
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data import build_songs_df, cosine_sim
from utils.styling import (
    plotly_template,
    render_highlight,
    render_module_header,
    render_success,
    render_warning,
)


FEATURES = ["danceability", "energy", "valence", "acousticness", "tempo_norm", "instrumentalness"]
FEATURE_LABELS = {
    "danceability": "Danceability",
    "energy": "Energy",
    "valence": "Mood Positif",
    "acousticness": "Akustik",
    "tempo_norm": "Tempo",
    "instrumentalness": "Instrumental",
}


def _radar_chart(profiles_dict, title=""):
    """Radar chart untuk beberapa profil sekaligus."""
    fig = go.Figure()
    labels = [FEATURE_LABELS[f] for f in FEATURES]
    colors = ["#1DB954", "#E50914", "#7C9EFF", "#F59E0B"]
    for i, (name, vals) in enumerate(profiles_dict.items()):
        fig.add_trace(go.Scatterpolar(
            r=list(vals) + [vals[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=name,
            line=dict(color=colors[i % len(colors)], width=2),
            opacity=0.7,
        ))
    fig.update_layout(
        **plotly_template()["layout"],
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#3A3F4A"),
            angularaxis=dict(gridcolor="#3A3F4A"),
            bgcolor="rgba(0,0,0,0)",
        ),
        height=380,
        margin=dict(l=20, r=20, t=30, b=20),
        title=title,
    )
    return fig


def _scatter_2d(songs_df, user_profile, top_indices, x_feat, y_feat):
    """Scatter plot 2D fitur lagu dengan top-N highlighted."""
    df = songs_df.copy()
    df["highlight"] = "Lagu lain"
    df.loc[top_indices, "highlight"] = "Top Rekomendasi"

    fig = px.scatter(
        df, x=x_feat, y=y_feat, color="highlight", hover_name="judul",
        hover_data=["artis", "genre"],
        color_discrete_map={"Lagu lain": "#5A6478", "Top Rekomendasi": "#1DB954"},
        size_max=15,
    )
    # User profile sebagai bintang besar
    fig.add_trace(go.Scatter(
        x=[user_profile[FEATURES.index(x_feat)]],
        y=[user_profile[FEATURES.index(y_feat)]],
        mode="markers+text",
        marker=dict(size=24, color="#E50914", symbol="star", line=dict(color="white", width=2)),
        text=["🎯 Anda"],
        textposition="top center",
        name="Profil Anda",
        showlegend=False,
    ))
    fig.update_layout(
        **plotly_template()["layout"],
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title=FEATURE_LABELS[x_feat],
        yaxis_title=FEATURE_LABELS[y_feat],
    )
    return fig


def _top_songs_chart(df_top):
    fig = go.Figure(go.Bar(
        x=df_top["similarity"],
        y=[f"{r['judul']} — {r['artis']}" for _, r in df_top.iterrows()],
        orientation="h",
        marker=dict(color="#1DB954"),
        text=[f"{v:.3f}" for v in df_top["similarity"]],
        textposition="outside",
    ))
    fig.update_layout(
        **plotly_template()["layout"],
        height=340,
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis_title="Cosine Similarity",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
    )
    return fig


def render():
    render_module_header(
        "spotify",
        "Spotify: AI-Driven Music Discovery",
        "Simulasi rekomendasi musik berbasis audio features dan mood profile",
    )

    with st.expander("📖 Penjelasan Teori (Klik untuk membuka)"):
        st.markdown(
            """
            Spotify menganalisis setiap lagu dan mengubahnya menjadi **vektor numerik**
            berisi sekitar 12 *audio features* yang diekstrak oleh AI dari sinyal audio:

            - **Danceability** (0–1): seberapa cocok untuk berdansa
            - **Energy** (0–1): intensitas dan kekuatan lagu
            - **Valence** (0–1): kepositifan emosional (0 sedih, 1 ceria)
            - **Acousticness** (0–1): seberapa akustik vs elektronik
            - **Tempo** (BPM): ketukan per menit
            - **Instrumentalness** (0–1): seberapa banyak instrumental vs vokal

            Lalu Spotify membangun **profil selera Anda** dari fitur lagu-lagu yang sering Anda dengar.
            Untuk merekomendasikan, Spotify mencari lagu lain yang vektornya paling dekat dengan profil
            Anda menggunakan **cosine similarity**.
            """
        )

    render_highlight(
        "💡 <strong>Cara menggunakan simulasi:</strong> Geser slider untuk membuat 'mood profile' "
        "Anda hari ini, lalu lihat lagu-lagu apa yang direkomendasikan dari katalog. "
        "Coba juga ubah slider <em>Eksplorasi</em> untuk menemukan lagu di luar zona nyaman!"
    )

    # ----- KONTROL: PRESET -----
    st.markdown("### 🎛️ Atur Mood Profile Anda")

    preset = st.radio(
        "🎯 Mulai dari preset (atau geser manual di bawah)",
        ["🔥 Workout", "😌 Chill", "🎉 Party", "📚 Belajar", "✍️ Custom"],
        horizontal=True,
        help="Preset akan mengatur slider otomatis. Pilih 'Custom' untuk atur sendiri.",
    )

    presets = {
        "🔥 Workout": [0.85, 0.90, 0.70, 0.05, 0.75, 0.10],
        "😌 Chill":   [0.40, 0.30, 0.55, 0.75, 0.30, 0.50],
        "🎉 Party":   [0.90, 0.85, 0.85, 0.05, 0.80, 0.05],
        "📚 Belajar": [0.30, 0.25, 0.45, 0.85, 0.25, 0.85],
    }
    defaults = presets.get(preset, [0.6, 0.6, 0.6, 0.3, 0.5, 0.2])

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        f_dance = st.slider("💃 Danceability", 0.0, 1.0, defaults[0], 0.05,
                            help="Seberapa cocok untuk berdansa. 0 = balada lambat, 1 = lagu dansa.")
        f_energy = st.slider("⚡ Energy", 0.0, 1.0, defaults[1], 0.05,
                             help="Intensitas dan kekuatan. 0 = lembut, 1 = penuh energi.")
    with c2:
        f_valence = st.slider("😊 Mood Positif (Valence)", 0.0, 1.0, defaults[2], 0.05,
                              help="0 = sedih/marah, 1 = ceria/bahagia.")
        f_acoustic = st.slider("🎻 Acousticness", 0.0, 1.0, defaults[3], 0.05,
                               help="0 = elektronik, 1 = akustik murni.")
    with c3:
        f_tempo = st.slider("🥁 Tempo (norm.)", 0.0, 1.0, defaults[4], 0.05,
                            help="Kecepatan ketukan. 0 = lambat (~60 BPM), 1 = cepat (~180 BPM).")
        f_instr = st.slider("🎹 Instrumentalness", 0.0, 1.0, defaults[5], 0.05,
                            help="0 = penuh vokal, 1 = instrumental murni.")

    user_profile = np.array([f_dance, f_energy, f_valence, f_acoustic, f_tempo, f_instr])

    # ----- FILTER GENRE -----
    songs_df = build_songs_df()
    all_genres = sorted(songs_df["genre"].unique().tolist())

    col_g, col_e = st.columns([1.3, 1])
    with col_g:
        selected_genres = st.multiselect(
            "🎼 Filter genre (opsional)",
            options=all_genres,
            default=all_genres,
            help="Batasi rekomendasi hanya pada genre tertentu. Kosongkan untuk pakai semua.",
        )
    with col_e:
        explorasi = st.slider(
            "🌍 Faktor Eksplorasi",
            0.0, 1.0, 0.2, 0.05,
            help="0 = hanya lagu paling mirip (eksploitasi). "
                 "1 = banyak lagu acak (eksplorasi). "
                 "Spotify Discover Weekly menggunakan faktor eksplorasi tinggi.",
        )

    if not selected_genres:
        selected_genres = all_genres

    st.markdown("---")

    # ----- RADAR CHART -----
    st.markdown("### 🎯 Mood Profile Anda")
    rerata_katalog = songs_df[FEATURES].mean().values

    fig_radar = _radar_chart({
        "Profil Anda": user_profile.tolist(),
        "Rerata Katalog": rerata_katalog.tolist(),
    })
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

    # ----- HITUNG SIMILARITY -----
    filtered = songs_df[songs_df["genre"].isin(selected_genres)].reset_index(drop=True)
    if len(filtered) == 0:
        st.error("Tidak ada lagu yang cocok dengan filter genre. Pilih minimal satu genre.")
        return

    sims = np.array([cosine_sim(user_profile, filtered.loc[i, FEATURES].values) for i in range(len(filtered))])

    # Tambahkan noise untuk simulasi eksplorasi
    if explorasi > 0:
        rng = np.random.default_rng(42)
        noise = rng.normal(0, explorasi * 0.15, size=len(sims))
        sims_final = sims + noise
    else:
        sims_final = sims

    filtered = filtered.copy()
    filtered["similarity"] = sims_final
    top = filtered.sort_values("similarity", ascending=False).head(8).reset_index()

    # ----- TOP REKOMENDASI -----
    st.markdown("### 🎧 Top 8 Lagu Rekomendasi")
    st.plotly_chart(_top_songs_chart(top), use_container_width=True, config={"displayModeBar": False})

    with st.expander("📊 Lihat tabel detail (fitur lengkap)"):
        df_show = top[["judul", "artis", "genre", "danceability", "energy", "valence",
                       "acousticness", "instrumentalness", "tempo", "similarity"]].copy()
        df_show.columns = ["Judul", "Artis", "Genre", "Dance", "Energy", "Valence",
                           "Acoustic", "Instr.", "Tempo (BPM)", "Similarity"]
        st.dataframe(
            df_show.style.format({
                "Dance": "{:.2f}", "Energy": "{:.2f}", "Valence": "{:.2f}",
                "Acoustic": "{:.2f}", "Instr.": "{:.2f}",
                "Tempo (BPM)": "{:.0f}", "Similarity": "{:.3f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

    # ----- SCATTER 2D -----
    st.markdown("### 🗺️ Visualisasi 2D Katalog Lagu")
    st.caption(
        "Setiap titik = satu lagu. Hijau = top rekomendasi, abu-abu = lagu lain. "
        "Bintang merah = profil Anda. Pilih dua fitur untuk dijadikan sumbu."
    )

    cc1, cc2 = st.columns(2)
    with cc1:
        x_feat = st.selectbox(
            "Sumbu X", FEATURES, index=1,
            format_func=lambda x: FEATURE_LABELS[x],
        )
    with cc2:
        y_feat = st.selectbox(
            "Sumbu Y", FEATURES, index=2,
            format_func=lambda x: FEATURE_LABELS[x],
        )

    top_idx_in_full = songs_df[songs_df["judul"].isin(top["judul"])].index.tolist()
    st.plotly_chart(
        _scatter_2d(songs_df, user_profile, top_idx_in_full, x_feat, y_feat),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    # ----- INSIGHT -----
    st.markdown("---")
    render_success(
        "🎓 <strong>Pelajaran kunci:</strong> Spotify mengubah lagu menjadi vektor angka, "
        "lalu menggunakan matematika sederhana (cosine similarity) untuk mencari yang 'mirip'. "
        "Coba ubah preset ke <em>Chill</em> lalu <em>Party</em> — Anda akan melihat lagu yang "
        "direkomendasikan berubah drastis sesuai mood profile!"
    )

    render_warning(
        "⚠️ <strong>Catatan:</strong> Spotify nyata menggunakan jauh lebih banyak fitur (~12+) "
        "dan menggabungkannya dengan <em>collaborative filtering</em> dari pola dengar 600+ juta pengguna. "
        "Discover Weekly menggunakan <em>Word2Vec</em>-like embeddings untuk menangkap konteks playlist."
    )
