"""
Modul Simulasi Netflix: Collaborative Filtering, Content-Based, dan Hybrid.

Pengguna bisa:
- Memilih user pembanding
- Mengubah algoritma rekomendasi
- Menyesuaikan parameter (jumlah neighbor, bobot CF vs CB)
- Melihat user-item matrix sebagai heatmap
- Melihat similarity antar user
- Mendapat Top-N rekomendasi beserta penjelasannya
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data import build_user_item_matrix, cosine_sim_matrix
from utils.styling import (
    plotly_template,
    render_concept_card,
    render_highlight,
    render_module_header,
    render_success,
    render_warning,
)


# ---------- ALGORITMA ----------

def collaborative_filtering(rating_matrix: pd.DataFrame, target_user: str, k_neighbors: int):
    """
    User-based Collaborative Filtering:
    1. Hitung cosine similarity target_user vs semua user lain.
    2. Ambil k_neighbors user paling mirip.
    3. Skor film = rata-rata tertimbang rating neighbor untuk film yang belum ditonton target.
    """
    R = rating_matrix.values
    users = rating_matrix.index.tolist()
    movies = rating_matrix.columns.tolist()
    idx = users.index(target_user)

    sim = cosine_sim_matrix(R)
    sim_target = sim[idx].copy()
    sim_target[idx] = -1  # exclude diri sendiri

    # Top-K tetangga
    neighbor_indices = np.argsort(-sim_target)[:k_neighbors]
    neighbor_sims = sim_target[neighbor_indices]

    # Film yang sudah ditonton target (rating > 0)
    watched_mask = R[idx] > 0
    unwatched_indices = np.where(~watched_mask)[0]

    scores = []
    for m in unwatched_indices:
        # Bobot rating tetangga yang sudah menonton film ini
        ratings = R[neighbor_indices, m]
        valid = ratings > 0
        if valid.sum() == 0:
            continue
        weighted = np.sum(ratings[valid] * neighbor_sims[valid])
        norm = np.sum(np.abs(neighbor_sims[valid]))
        if norm == 0:
            continue
        scores.append((movies[m], weighted / norm, neighbor_sims[valid].mean()))

    df = pd.DataFrame(scores, columns=["judul", "skor_cf", "avg_neighbor_sim"])
    return df, sim_target, neighbor_indices


def content_based(movies_df: pd.DataFrame, rating_matrix: pd.DataFrame, target_user: str):
    """
    Content-Based:
    1. Bangun profil user = rata-rata fitur konten dari film yang dirating tinggi (>=4).
    2. Skor film = cosine similarity antara fitur film dan profil user.
    """
    # Encoding genre sebagai one-hot
    all_genres = sorted(set(movies_df["genre_primer"]).union(set(movies_df["genre_sekunder"])))
    feat = np.zeros((len(movies_df), len(all_genres) + 1))
    for i, row in movies_df.iterrows():
        feat[i, all_genres.index(row["genre_primer"])] = 1.0
        feat[i, all_genres.index(row["genre_sekunder"])] = 0.6
        feat[i, -1] = (row["tahun"] - 2010) / 15.0  # tahun ternormalisasi

    R = rating_matrix.values
    users = rating_matrix.index.tolist()
    idx = users.index(target_user)
    user_ratings = R[idx]

    # Profil user = rata-rata fitur film yang dirating tinggi
    liked_mask = user_ratings >= 4
    if liked_mask.sum() == 0:
        # fallback: pakai semua yang sudah dirating
        liked_mask = user_ratings > 0
    profile = feat[liked_mask].mean(axis=0)

    # Cosine similarity profil vs setiap film
    norm_p = np.linalg.norm(profile) + 1e-9
    profile_norm = profile / norm_p
    feat_norms = np.linalg.norm(feat, axis=1, keepdims=True) + 1e-9
    feat_normed = feat / feat_norms
    sim_scores = feat_normed @ profile_norm

    # Konversi ke skala rating 1-5 untuk konsistensi
    sim_scores = 1 + 4 * (sim_scores - sim_scores.min()) / (sim_scores.max() - sim_scores.min() + 1e-9)

    # Hanya film yang belum ditonton
    unwatched = user_ratings == 0
    df = pd.DataFrame({
        "judul": movies_df["judul"].values,
        "skor_cb": sim_scores,
        "unwatched": unwatched,
    })
    df = df[df["unwatched"]].drop(columns=["unwatched"])
    return df


# ---------- VISUALISASI ----------

def render_rating_heatmap(rating_matrix: pd.DataFrame, target_user: str):
    """Heatmap user-item matrix dengan target user di-highlight."""
    fig = px.imshow(
        rating_matrix.values,
        labels=dict(x="Film", y="Pengguna", color="Rating"),
        x=rating_matrix.columns,
        y=rating_matrix.index,
        color_continuous_scale=[[0, "#1A1D24"], [0.01, "#3A2A3F"], [0.5, "#7C3F8F"], [1, "#E50914"]],
        aspect="auto",
        zmin=0, zmax=5,
    )
    fig.update_layout(
        **plotly_template()["layout"],
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_xaxes(tickangle=-45)

    # Highlight target user
    idx = list(rating_matrix.index).index(target_user)
    fig.add_shape(
        type="rect",
        x0=-0.5, x1=len(rating_matrix.columns) - 0.5,
        y0=idx - 0.5, y1=idx + 0.5,
        line=dict(color="#FFD60A", width=3),
        fillcolor="rgba(0,0,0,0)",
    )
    return fig


def render_similarity_bar(sim_array, user_names, target_user, top_k):
    """Bar chart similarity antar user terhadap target."""
    df = pd.DataFrame({"user": user_names, "similarity": sim_array})
    df = df[df["user"] != target_user].sort_values("similarity", ascending=True)
    colors = ["#7C9EFF" if i < (len(df) - top_k) else "#E50914" for i in range(len(df))]

    fig = go.Figure(go.Bar(
        x=df["similarity"],
        y=df["user"],
        orientation="h",
        marker=dict(color=colors),
        text=[f"{v:.2f}" for v in df["similarity"]],
        textposition="outside",
    ))
    fig.update_layout(
        **plotly_template()["layout"],
        height=320,
        margin=dict(l=10, r=30, t=20, b=10),
        xaxis_title="Cosine Similarity",
        yaxis_title="",
        xaxis=dict(range=[0, 1.05]),
    )
    return fig


def render_recommendations_chart(df_recs: pd.DataFrame, score_col: str, color: str):
    df = df_recs.head(8).sort_values(score_col, ascending=True)
    fig = go.Figure(go.Bar(
        x=df[score_col],
        y=df["judul"],
        orientation="h",
        marker=dict(color=color),
        text=[f"{v:.2f}" for v in df[score_col]],
        textposition="outside",
    ))
    fig.update_layout(
        **plotly_template()["layout"],
        height=340,
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis_title="Skor Prediksi",
        yaxis_title="",
    )
    return fig


# ---------- HALAMAN UTAMA ----------

def render():
    render_module_header(
        "netflix",
        "Netflix: AI-Powered Personalization",
        "Simulasi Collaborative Filtering, Content-Based, dan Hybrid untuk rekomendasi film & serial",
    )

    # PENJELASAN SINGKAT
    with st.expander("📖 Penjelasan Teori (Klik untuk membuka)"):
        st.markdown(
            """
            Netflix menggunakan kombinasi beberapa algoritma untuk merekomendasikan tayangan.
            Dua yang paling fundamental adalah:

            **1. Collaborative Filtering (CF)** — Mencari pengguna lain yang seleranya mirip
            dengan Anda. Jika tetangga-tetangga Anda menyukai sebuah film tetapi Anda belum
            menontonnya, kemungkinan besar Anda juga akan menyukainya.

            **2. Content-Based Filtering (CB)** — Membangun profil selera Anda berdasarkan
            ciri film yang Anda sukai (genre, tahun, dll.), lalu mencari film lain dengan
            ciri serupa.

            **3. Hybrid** — Menggabungkan kedua skor di atas dengan bobot tertentu untuk
            mendapatkan rekomendasi yang lebih robust.
            """
        )

    render_highlight(
        "💡 <strong>Cara menggunakan simulasi ini:</strong> Pilih satu pengguna sebagai 'Anda', "
        "lalu atur algoritma dan parameternya di kontrol di bawah. Lihat bagaimana rekomendasi "
        "berubah saat parameter diubah!"
    )

    # ----- DATA -----
    rating_matrix, movies_df, profiles = build_user_item_matrix()
    user_names = rating_matrix.index.tolist()

    # ----- KONTROL -----
    st.markdown("### 🎛️ Kontrol Simulasi")
    col_a, col_b, col_c = st.columns([1.2, 1, 1])
    with col_a:
        target_user = st.selectbox(
            "👤 Pilih pengguna",
            options=user_names,
            index=0,
            help="Pengguna yang akan menjadi target rekomendasi. "
                 "Setiap pengguna memiliki preferensi genre yang berbeda.",
        )
    with col_b:
        algoritma = st.radio(
            "🧠 Algoritma",
            ["Collaborative Filtering", "Content-Based", "Hybrid"],
            help="CF = berdasarkan user mirip; CB = berdasarkan konten serupa; Hybrid = gabungan.",
        )
    with col_c:
        k_neighbors = st.slider(
            "👥 Jumlah neighbor (k)",
            min_value=2, max_value=6, value=3,
            help="Berapa banyak pengguna paling mirip yang dipakai untuk CF. "
                 "Nilai kecil = personal tapi mudah salah; besar = stabil tapi generik.",
        )

    bobot_cf = 0.5
    if algoritma == "Hybrid":
        bobot_cf = st.slider(
            "⚖️ Bobot Collaborative Filtering (sisanya = Content-Based)",
            min_value=0.0, max_value=1.0, value=0.5, step=0.05,
            help="0 = hanya konten; 1 = hanya kolaboratif; 0.5 = seimbang.",
        )

    # Tampilkan profil user
    profile = next(p for p in profiles if p["name"] == target_user)
    st.markdown(
        f"<div class='success-box'>👤 <strong>{target_user}</strong> menyukai genre: "
        f"{', '.join(profile['fav_genres'])}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ----- VISUALISASI MATRIX -----
    st.markdown("### 🗺️ User-Item Matrix")
    st.caption(
        "Setiap baris adalah pengguna, setiap kolom adalah film. "
        "Warna sel = rating 1–5 (gelap = belum nonton). "
        "Baris kuning = pengguna yang Anda pilih."
    )
    st.plotly_chart(
        render_rating_heatmap(rating_matrix, target_user),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    # ----- SIMILARITY -----
    st.markdown("### 🔗 Kemiripan Antar Pengguna")
    st.caption(
        f"Cosine similarity {target_user} dengan pengguna lain. "
        f"Bar merah = {k_neighbors} pengguna paling mirip (digunakan oleh CF)."
    )

    sim_matrix = cosine_sim_matrix(rating_matrix.values)
    target_idx = user_names.index(target_user)
    sim_target = sim_matrix[target_idx].copy()
    st.plotly_chart(
        render_similarity_bar(sim_target, user_names, target_user, k_neighbors),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.markdown("---")

    # ----- HITUNG REKOMENDASI -----
    st.markdown(f"### 🎯 Top Rekomendasi untuk **{target_user}**")

    df_cf, _, _ = collaborative_filtering(rating_matrix, target_user, k_neighbors)
    df_cb = content_based(movies_df, rating_matrix, target_user)

    if algoritma == "Collaborative Filtering":
        df_final = df_cf.copy().sort_values("skor_cf", ascending=False)
        st.plotly_chart(
            render_recommendations_chart(df_final, "skor_cf", "#E50914"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        with st.expander("📊 Lihat detail skor & alasan"):
            df_show = df_final.head(10).copy()
            df_show.columns = ["Judul", "Skor CF", "Rerata Similarity Neighbor"]
            st.dataframe(df_show, use_container_width=True, hide_index=True)

    elif algoritma == "Content-Based":
        df_final = df_cb.copy().sort_values("skor_cb", ascending=False)
        st.plotly_chart(
            render_recommendations_chart(df_final, "skor_cb", "#7C9EFF"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        with st.expander("📊 Lihat detail skor & alasan"):
            df_show = df_final.head(10).copy()
            df_show.columns = ["Judul", "Skor CB (kemiripan konten)"]
            st.dataframe(df_show, use_container_width=True, hide_index=True)

    else:  # Hybrid
        # Normalisasi skor 0-1 dulu agar bisa dijumlah
        cf_norm = df_cf.set_index("judul")["skor_cf"]
        cb_norm = df_cb.set_index("judul")["skor_cb"]
        joined = pd.DataFrame({"cf": cf_norm, "cb": cb_norm}).dropna()
        joined["cf_n"] = (joined["cf"] - joined["cf"].min()) / (joined["cf"].max() - joined["cf"].min() + 1e-9)
        joined["cb_n"] = (joined["cb"] - joined["cb"].min()) / (joined["cb"].max() - joined["cb"].min() + 1e-9)
        joined["skor_hybrid"] = bobot_cf * joined["cf_n"] + (1 - bobot_cf) * joined["cb_n"]
        joined = joined.sort_values("skor_hybrid", ascending=False).reset_index()
        joined.rename(columns={"index": "judul"}, inplace=True)

        st.plotly_chart(
            render_recommendations_chart(joined, "skor_hybrid", "#8B5CF6"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        with st.expander("📊 Lihat detail skor hybrid"):
            df_show = joined.head(10)[["judul", "cf_n", "cb_n", "skor_hybrid"]].copy()
            df_show.columns = ["Judul", "Skor CF (norm)", "Skor CB (norm)", "Skor Hybrid"]
            st.dataframe(df_show.style.format({
                "Skor CF (norm)": "{:.3f}",
                "Skor CB (norm)": "{:.3f}",
                "Skor Hybrid": "{:.3f}",
            }), use_container_width=True, hide_index=True)

    # ----- INSIGHT -----
    st.markdown("---")
    render_success(
        f"🎓 <strong>Pelajaran kunci:</strong> Coba ganti pengguna ke <em>{user_names[1]}</em> atau "
        f"<em>{user_names[2]}</em>, lalu bandingkan rekomendasi yang dihasilkan. "
        f"Anda akan melihat bahwa preferensi genre setiap pengguna membentuk pola rekomendasi yang berbeda. "
        f"Inilah inti dari personalisasi AI!"
    )

    render_warning(
        "⚠️ <strong>Catatan implementasi nyata:</strong> Netflix sesungguhnya menggunakan "
        "<em>matrix factorization</em> dan <em>deep neural networks</em> dengan miliaran parameter, "
        "bukan sekadar cosine similarity. Namun konsep dasarnya sama: cari pola kemiripan antara pengguna dan konten."
    )
