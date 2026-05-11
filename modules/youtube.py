"""
Modul Simulasi YouTube: Two-Stage Pipeline (Candidate Generation + Ranking).

Pengguna bisa:
- Memilih kategori minat
- Mengatur bobot tiap sinyal engagement (watch_time, CTR, likes, freshness)
- Mengatur faktor diversitas
- Melihat pipeline diagram
- Melihat ranking score breakdown per video
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data import build_videos_df
from utils.styling import (
    plotly_template,
    render_highlight,
    render_module_header,
    render_success,
    render_warning,
)


def _pipeline_diagram():
    """Diagram dua tahap pipeline YouTube."""
    fig = go.Figure()

    boxes = [
        {"x": 0.08, "y": 0.5, "label": "Katalog<br>Penuh<br><b>1B+ video</b>", "color": "#5A6478"},
        {"x": 0.35, "y": 0.5, "label": "Candidate<br>Generation<br>(filter kategori,<br>history, popularitas)", "color": "#7C9EFF"},
        {"x": 0.62, "y": 0.5, "label": "~100 Kandidat", "color": "#F59E0B"},
        {"x": 0.85, "y": 0.5, "label": "Ranking<br>(multi-signal<br>scoring)", "color": "#FF0000"},
    ]
    for b in boxes:
        fig.add_shape(
            type="rect",
            x0=b["x"] - 0.07, x1=b["x"] + 0.07,
            y0=b["y"] - 0.18, y1=b["y"] + 0.18,
            fillcolor=b["color"], line=dict(color="white", width=2),
        )
        fig.add_annotation(
            x=b["x"], y=b["y"], text=b["label"],
            showarrow=False, font=dict(color="white", size=11),
        )

    # Arrows
    for i in range(len(boxes) - 1):
        fig.add_annotation(
            x=boxes[i+1]["x"] - 0.07,
            y=0.5,
            ax=boxes[i]["x"] + 0.07,
            ay=0.5,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2,
            arrowcolor="#9CA3AF",
        )

    # Output: top-N
    fig.add_shape(
        type="rect",
        x0=0.85 - 0.07, x1=0.85 + 0.07,
        y0=0.08, y1=0.32,
        fillcolor="#10B981", line=dict(color="white", width=2),
    )
    fig.add_annotation(x=0.85, y=0.20, text="Top-N<br>Tampilan<br>Beranda",
                       showarrow=False, font=dict(color="white", size=11))
    fig.add_annotation(
        x=0.85, y=0.32, ax=0.85, ay=0.32 + 0.18,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2,
        arrowcolor="#9CA3AF",
    )

    fig.update_layout(
        **plotly_template()["layout"],
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
    )
    return fig


def _ranking_breakdown_chart(df_top, weights):
    """Stacked bar: kontribusi setiap sinyal pada total skor per video."""
    df = df_top.head(8).copy()

    components = {
        "Watch Completion": df["watch_completion"] * weights["watch"],
        "CTR": df["ctr_norm"] * weights["ctr"],
        "Like Ratio": df["like_ratio"] * weights["like"],
        "Freshness": df["freshness_score"] * weights["fresh"],
        "Popularity": df["popularity_norm"] * weights["pop"],
    }

    fig = go.Figure()
    colors = {"Watch Completion": "#FF0000", "CTR": "#7C9EFF",
              "Like Ratio": "#1DB954", "Freshness": "#F59E0B", "Popularity": "#8B5CF6"}
    for name, vals in components.items():
        fig.add_trace(go.Bar(
            name=name,
            y=df["judul"],
            x=vals,
            orientation="h",
            marker_color=colors[name],
        ))
    fig.update_layout(
        **plotly_template()["layout"],
        barmode="stack",
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Kontribusi Skor",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def _candidate_pool_chart(df_all, df_candidates):
    """Scatter: views vs watch_completion, candidates highlighted."""
    df = df_all.copy()
    df["status"] = "Tidak Lolos Filter"
    df.loc[df["id"].isin(df_candidates["id"]), "status"] = "Lolos Filter (Kandidat)"

    fig = px.scatter(
        df,
        x="views_juta", y="watch_completion",
        color="status",
        hover_name="judul",
        hover_data=["kategori"],
        color_discrete_map={
            "Tidak Lolos Filter": "#5A6478",
            "Lolos Filter (Kandidat)": "#FF0000",
        },
        size="durasi_menit",
        size_max=20,
    )
    fig.update_layout(
        **plotly_template()["layout"],
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Views (juta)",
        yaxis_title="Watch Completion Rate",
    )
    return fig


def render():
    render_module_header(
        "youtube",
        "YouTube: AI-Enhanced Video Recommendations",
        "Simulasi pipeline dua tahap — candidate generation diikuti ranking multi-signal",
    )

    with st.expander("📖 Penjelasan Teori (Klik untuk membuka)"):
        st.markdown(
            """
            YouTube menggunakan **pipeline dua tahap** untuk merekomendasikan video:

            **Tahap 1 — Candidate Generation:** Dari miliaran video di YouTube, filter cepat ke
            sekitar 100–500 video yang *mungkin* relevan untuk pengguna. Filter ini menggunakan
            kategori minat, riwayat tontonan, dan sinyal popularitas.

            **Tahap 2 — Ranking:** Dari ~100 kandidat tersebut, hitung skor relevansi yang lebih
            mendalam menggunakan banyak sinyal:

            - **Watch Completion Rate** — berapa persen rata-rata pengguna menyelesaikan video
            - **Click-Through Rate (CTR)** — berapa persen yang klik dari thumbnail
            - **Like Ratio** — rasio like terhadap total reaksi
            - **Freshness** — seberapa baru video tersebut diunggah
            - **Popularity** — jumlah views

            Setiap sinyal diberi bobot. Skor akhir = jumlah tertimbang dari semua sinyal.
            Video dengan skor tertinggi muncul di beranda Anda.
            """
        )

    # Pipeline diagram
    st.markdown("### 🔄 Pipeline Rekomendasi YouTube")
    st.plotly_chart(_pipeline_diagram(), use_container_width=True, config={"displayModeBar": False})

    render_highlight(
        "💡 <strong>Cara menggunakan simulasi:</strong> Pilih kategori yang Anda minati, "
        "lalu atur bobot setiap sinyal di sisi kanan. Lihat bagaimana komposisi video di "
        "rekomendasi berubah berdasarkan apa yang Anda anggap penting!"
    )

    # ----- KONTROL -----
    st.markdown("### 🎛️ Kontrol Simulasi")

    videos_df = build_videos_df()
    all_categories = sorted(videos_df["kategori"].unique().tolist())

    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        st.markdown("**📂 Tahap 1: Kategori Minat**")
        st.caption("YouTube akan memprioritaskan video dari kategori yang Anda pilih.")
        selected_cats = st.multiselect(
            "Pilih kategori",
            options=all_categories,
            default=["Edukasi", "Tutorial"],
            help="Berfungsi sebagai filter awal di tahap candidate generation.",
        )
        min_completion = st.slider(
            "Filter minimum watch completion",
            0.0, 1.0, 0.5, 0.05,
            help="Hanya video dengan watch completion ≥ nilai ini yang lolos filter awal.",
        )

    with col_r:
        st.markdown("**⚖️ Tahap 2: Bobot Sinyal Ranking**")
        st.caption("Atur seberapa penting masing-masing sinyal (total tidak harus 1, akan dinormalisasi).")
        w_watch = st.slider("👀 Watch Completion",      0.0, 1.0, 0.35, 0.05,
                            help="Bobot untuk persentase penonton yang menyelesaikan video.")
        w_ctr   = st.slider("🖱️ Click-Through Rate",   0.0, 1.0, 0.20, 0.05,
                            help="Bobot untuk persentase klik dari impresi thumbnail.")
        w_like  = st.slider("👍 Like Ratio",            0.0, 1.0, 0.15, 0.05,
                            help="Bobot untuk rasio like.")
        w_fresh = st.slider("⏱️ Freshness",             0.0, 1.0, 0.20, 0.05,
                            help="Bobot untuk seberapa baru video diunggah.")
        w_pop   = st.slider("🔥 Popularity (Views)",    0.0, 1.0, 0.10, 0.05,
                            help="Bobot untuk jumlah views total.")

    if not selected_cats:
        st.error("Pilih minimal satu kategori minat untuk melanjutkan.")
        return

    st.markdown("---")

    # ----- TAHAP 1: CANDIDATE GENERATION -----
    candidates = videos_df[
        (videos_df["kategori"].isin(selected_cats)) &
        (videos_df["watch_completion"] >= min_completion)
    ].copy()

    st.markdown("### 📥 Tahap 1: Candidate Generation")
    cc1, cc2 = st.columns(2)
    with cc1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="label">Katalog Total</div>
                <div class="value">{len(videos_df)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cc2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="label">Lolos Filter (Kandidat)</div>
                <div class="value">{len(candidates)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.plotly_chart(
        _candidate_pool_chart(videos_df, candidates),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    if len(candidates) == 0:
        st.warning("Tidak ada video lolos filter. Longgarkan kriteria di kiri.")
        return

    # ----- TAHAP 2: RANKING -----
    st.markdown("### 🎯 Tahap 2: Multi-Signal Ranking")

    # Normalisasi fitur ke 0-1
    candidates["ctr_norm"] = (candidates["ctr"] - videos_df["ctr"].min()) / (videos_df["ctr"].max() - videos_df["ctr"].min())
    candidates["freshness_score"] = np.exp(-candidates["freshness_hari"] / 30.0)  # decay exponensial
    candidates["popularity_norm"] = (candidates["views_juta"] - videos_df["views_juta"].min()) / (videos_df["views_juta"].max() - videos_df["views_juta"].min())

    # Normalisasi bobot
    total_w = w_watch + w_ctr + w_like + w_fresh + w_pop + 1e-9
    weights = {
        "watch": w_watch / total_w,
        "ctr":   w_ctr   / total_w,
        "like":  w_like  / total_w,
        "fresh": w_fresh / total_w,
        "pop":   w_pop   / total_w,
    }

    candidates["ranking_score"] = (
        candidates["watch_completion"] * weights["watch"]
        + candidates["ctr_norm"] * weights["ctr"]
        + candidates["like_ratio"] * weights["like"]
        + candidates["freshness_score"] * weights["fresh"]
        + candidates["popularity_norm"] * weights["pop"]
    )

    top = candidates.sort_values("ranking_score", ascending=False).reset_index(drop=True)

    st.caption(
        "Setiap bar menunjukkan kontribusi tiap sinyal terhadap skor akhir. "
        "Coba naikkan bobot **Freshness** untuk melihat video baru naik peringkat, "
        "atau **Popularity** untuk video viral."
    )
    st.plotly_chart(
        _ranking_breakdown_chart(top, weights),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    # Tabel lengkap
    with st.expander("📊 Lihat tabel detail Top-10 rekomendasi"):
        df_show = top[["judul", "kategori", "ranking_score", "watch_completion",
                       "ctr", "like_ratio", "freshness_hari", "views_juta"]].head(10).copy()
        df_show.columns = ["Judul", "Kategori", "Skor Akhir", "Watch %", "CTR",
                           "Like Ratio", "Umur (hari)", "Views (jt)"]
        st.dataframe(
            df_show.style.format({
                "Skor Akhir": "{:.3f}",
                "Watch %": "{:.0%}",
                "CTR": "{:.0%}",
                "Like Ratio": "{:.0%}",
                "Views (jt)": "{:.1f}",
            }).background_gradient(subset=["Skor Akhir"], cmap="Reds"),
            use_container_width=True,
            hide_index=True,
        )

    # Bobot saat ini
    st.markdown("**📐 Bobot Ternormalisasi Saat Ini:**")
    fig_w = go.Figure(go.Bar(
        x=list(weights.values()),
        y=["Watch Completion", "CTR", "Like Ratio", "Freshness", "Popularity"],
        orientation="h",
        marker=dict(color=["#FF0000", "#7C9EFF", "#1DB954", "#F59E0B", "#8B5CF6"]),
        text=[f"{v:.1%}" for v in weights.values()],
        textposition="outside",
    ))
    fig_w.update_layout(
        **plotly_template()["layout"],
        height=220,
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis_title="", yaxis_title="",
        xaxis=dict(range=[0, 0.55], tickformat=".0%"),
    )
    st.plotly_chart(fig_w, use_container_width=True, config={"displayModeBar": False})

    # ----- INSIGHT -----
    st.markdown("---")
    render_success(
        "🎓 <strong>Pelajaran kunci:</strong> Tidak ada satu sinyal pun yang 'sempurna'. "
        "YouTube menggunakan banyak sinyal sekaligus karena: video populer belum tentu Anda suka, "
        "video baru belum punya data engagement, dan watch time tinggi pada video pendek tidak "
        "sebanding dengan watch time pada video panjang. <strong>Coba geser bobot Freshness ke 1.0</strong> — "
        "lihat bagaimana video terbaru langsung naik peringkat!"
    )

    render_warning(
        "⚠️ <strong>Catatan implementasi nyata:</strong> YouTube menggunakan <em>Deep Neural Network</em> "
        "(Two-Tower Model dari paper Covington et al., 2016) untuk candidate generation, dan "
        "<em>Multi-task Learning</em> untuk ranking — yang memprediksi beberapa target sekaligus "
        "(klik, watch time, like). Bobot tidak diatur manual, tapi <em>dipelajari</em> dari data eksperimen."
    )
