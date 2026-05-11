"""
Generator data sintetis untuk simulasi rekomendasi.

Semua data bersifat fiktif tapi merefleksikan struktur data nyata di Netflix/Spotify/YouTube.
"""

import numpy as np
import pandas as pd


# ========== NETFLIX DATASET ==========

MOVIES = [
    # (judul, genre_primer, genre_sekunder, tahun, rating_rerata, popularitas)
    ("Stranger Things",        "Sci-Fi",   "Horror",    2016, 4.7, 95),
    ("The Crown",              "Drama",    "Sejarah",   2016, 4.5, 78),
    ("Money Heist",            "Crime",    "Thriller",  2017, 4.6, 92),
    ("Squid Game",             "Thriller", "Drama",     2021, 4.5, 98),
    ("Wednesday",              "Misteri",  "Komedi",    2022, 4.4, 90),
    ("The Witcher",            "Fantasi",  "Aksi",      2019, 4.2, 85),
    ("Bridgerton",             "Romance",  "Drama",     2020, 4.3, 82),
    ("Dark",                   "Sci-Fi",   "Misteri",   2017, 4.7, 80),
    ("Narcos",                 "Crime",    "Drama",     2015, 4.6, 75),
    ("Ozark",                  "Crime",    "Thriller",  2017, 4.5, 73),
    ("The Queen's Gambit",     "Drama",    "Sejarah",   2020, 4.6, 86),
    ("Lupin",                  "Crime",    "Misteri",   2021, 4.3, 70),
    ("Black Mirror",           "Sci-Fi",   "Thriller",  2011, 4.5, 88),
    ("Peaky Blinders",         "Crime",    "Sejarah",   2013, 4.6, 84),
    ("Cobra Kai",              "Aksi",     "Komedi",    2018, 4.4, 76),
    ("Emily in Paris",         "Romance",  "Komedi",    2020, 3.9, 72),
    ("All of Us Are Dead",     "Horror",   "Thriller",  2022, 4.1, 79),
    ("Vincenzo",               "Crime",    "Komedi",    2021, 4.5, 74),
    ("The Good Place",         "Komedi",   "Fantasi",   2016, 4.5, 68),
    ("Mindhunter",             "Crime",    "Drama",     2017, 4.6, 66),
]


def build_movies_df():
    df = pd.DataFrame(
        MOVIES,
        columns=["judul", "genre_primer", "genre_sekunder", "tahun", "rating", "popularitas"],
    )
    df["id"] = range(len(df))
    return df


def build_user_item_matrix(seed=42, n_users=8):
    """
    Bangun user-item matrix sintetis untuk demonstrasi Collaborative Filtering.
    Rating 1-5, 0 = belum nonton.
    """
    rng = np.random.default_rng(seed)
    movies = build_movies_df()
    n_movies = len(movies)

    # Profil user yang berbeda-beda agar similarity-nya terlihat jelas
    user_profiles = [
        {"name": "Andi",   "fav_genres": ["Sci-Fi", "Thriller"]},
        {"name": "Budi",   "fav_genres": ["Romance", "Komedi"]},
        {"name": "Citra",  "fav_genres": ["Crime", "Thriller"]},
        {"name": "Dewi",   "fav_genres": ["Sci-Fi", "Misteri"]},
        {"name": "Eko",    "fav_genres": ["Aksi", "Fantasi"]},
        {"name": "Fitri",  "fav_genres": ["Drama", "Sejarah"]},
        {"name": "Gita",   "fav_genres": ["Komedi", "Romance"]},
        {"name": "Hadi",   "fav_genres": ["Horror", "Sci-Fi"]},
    ][:n_users]

    matrix = np.zeros((n_users, n_movies))
    for i, profile in enumerate(user_profiles):
        for j, row in movies.iterrows():
            # Skip random ~30% films (belum ditonton)
            if rng.random() < 0.3:
                continue
            # Rating dasar berdasar genre match
            match = 0
            if row["genre_primer"] in profile["fav_genres"]:
                match += 2
            if row["genre_sekunder"] in profile["fav_genres"]:
                match += 1
            base = 2.5 + match * 0.6
            noise = rng.normal(0, 0.4)
            rating = float(np.clip(round(base + noise), 1, 5))
            matrix[i, j] = rating

    user_names = [p["name"] for p in user_profiles]
    df = pd.DataFrame(matrix, index=user_names, columns=movies["judul"].tolist())
    return df, movies, user_profiles


# ========== SPOTIFY DATASET ==========

SONGS = [
    # (judul, artis, genre, danceability, energy, valence, acousticness, tempo, instrumentalness)
    ("Blinding Lights",      "The Weeknd",      "Pop",        0.85, 0.73, 0.33, 0.00, 171, 0.00),
    ("As It Was",            "Harry Styles",    "Pop",        0.52, 0.73, 0.66, 0.34, 174, 0.00),
    ("Levitating",           "Dua Lipa",        "Pop",        0.88, 0.82, 0.92, 0.01, 103, 0.00),
    ("Bohemian Rhapsody",    "Queen",           "Rock",       0.39, 0.40, 0.23, 0.29, 144, 0.00),
    ("Smells Like Teen Spirit","Nirvana",       "Rock",       0.50, 0.91, 0.72, 0.00, 117, 0.00),
    ("Hotel California",     "Eagles",          "Rock",       0.58, 0.50, 0.61, 0.02, 147, 0.00),
    ("Lose Yourself",        "Eminem",          "Hip-Hop",    0.69, 0.91, 0.46, 0.07,  86, 0.00),
    ("Sicko Mode",           "Travis Scott",    "Hip-Hop",    0.83, 0.73, 0.45, 0.00, 155, 0.00),
    ("HUMBLE.",              "Kendrick Lamar",  "Hip-Hop",    0.91, 0.62, 0.42, 0.00, 150, 0.00),
    ("Take Five",            "Dave Brubeck",    "Jazz",       0.55, 0.34, 0.71, 0.55, 174, 0.65),
    ("So What",              "Miles Davis",     "Jazz",       0.42, 0.32, 0.40, 0.78, 138, 0.71),
    ("Strobe",               "Deadmau5",        "Elektronik", 0.62, 0.71, 0.21, 0.00, 128, 0.92),
    ("Strobe Lights",        "Calvin Harris",   "Elektronik", 0.78, 0.84, 0.55, 0.00, 128, 0.04),
    ("Clair de Lune",        "Debussy",         "Klasik",     0.20, 0.05, 0.13, 0.98,  70, 0.95),
    ("Moonlight Sonata",     "Beethoven",       "Klasik",     0.18, 0.10, 0.10, 0.97,  60, 0.94),
    ("Despacito",            "Luis Fonsi",      "Latin",      0.66, 0.78, 0.83, 0.21, 178, 0.00),
    ("Bad Bunny - Tití Me",  "Bad Bunny",       "Latin",      0.65, 0.71, 0.54, 0.09, 107, 0.00),
    ("Shape of You",         "Ed Sheeran",      "Pop",        0.83, 0.65, 0.93, 0.58,  96, 0.00),
    ("Counting Stars",       "OneRepublic",     "Pop",        0.66, 0.70, 0.48, 0.07, 122, 0.00),
    ("Riders on the Storm",  "The Doors",       "Rock",       0.50, 0.49, 0.43, 0.42, 113, 0.32),
    ("Take On Me",           "a-ha",            "Pop",        0.57, 0.89, 0.88, 0.00, 169, 0.01),
    ("Mr. Brightside",       "The Killers",     "Rock",       0.36, 0.91, 0.23, 0.00, 148, 0.00),
    ("One Dance",            "Drake",           "Hip-Hop",    0.79, 0.62, 0.37, 0.00, 104, 0.00),
    ("Watermelon Sugar",     "Harry Styles",    "Pop",        0.55, 0.82, 0.56, 0.12,  95, 0.00),
]


def build_songs_df():
    cols = ["judul", "artis", "genre", "danceability", "energy", "valence",
            "acousticness", "tempo", "instrumentalness"]
    df = pd.DataFrame(SONGS, columns=cols)
    df["id"] = range(len(df))
    # Normalisasi tempo ke 0-1
    df["tempo_norm"] = (df["tempo"] - df["tempo"].min()) / (df["tempo"].max() - df["tempo"].min())
    return df


# ========== YOUTUBE DATASET ==========

VIDEOS = [
    # (judul, kategori, durasi_menit, views_juta, like_ratio, ctr, watch_completion, freshness_hari)
    ("Cara Setup Streamlit di GitHub",        "Tutorial",    12,  0.8, 0.96, 0.08, 0.78,  14),
    ("Python untuk Pemula 2025",              "Tutorial",    25,  3.2, 0.94, 0.07, 0.71,  60),
    ("Reaksi Lagu Spotify Wrapped",           "Hiburan",      8,  2.1, 0.92, 0.11, 0.82,   7),
    ("Review Film Terbaru Netflix",           "Hiburan",     15,  1.5, 0.89, 0.10, 0.74,   3),
    ("Vlog Liburan ke Bali",                  "Vlog",        18,  0.9, 0.91, 0.06, 0.65,  20),
    ("Berita Teknologi Hari Ini",             "Berita",       6,  0.5, 0.85, 0.09, 0.60,   1),
    ("Update AI: GPT vs Claude",              "Berita",      10,  1.2, 0.93, 0.12, 0.83,   2),
    ("Tips Belajar Coding Otodidak",          "Edukasi",     14,  2.5, 0.97, 0.09, 0.79,  45),
    ("Mengajar AI ke Anak SD",                "Edukasi",     20,  0.4, 0.95, 0.05, 0.72,  30),
    ("Resep Nasi Goreng Restoran",            "Lifestyle",    9,  1.8, 0.93, 0.10, 0.81,  15),
    ("Workout Pemula 15 Menit",               "Lifestyle",   15,  2.2, 0.95, 0.08, 0.76,  25),
    ("Gaming: Free Fire Highlight",           "Gaming",       7,  4.5, 0.91, 0.13, 0.85,   5),
    ("Tutorial Mobile Legend",                "Gaming",      11,  3.1, 0.92, 0.11, 0.78,  10),
    ("Diskusi Kurikulum Merdeka",             "Edukasi",     28,  0.3, 0.93, 0.04, 0.58, 100),
    ("Tutorial Editing Capcut",               "Tutorial",    13,  2.7, 0.96, 0.09, 0.80,  18),
    ("Podcast: Masa Depan AI di Pendidikan",  "Edukasi",     45,  0.6, 0.94, 0.05, 0.55,  40),
    ("Stand Up Comedy Special",               "Hiburan",     22,  1.9, 0.94, 0.10, 0.77,  12),
    ("Tour Kampus BINUS",                     "Edukasi",      8,  0.7, 0.93, 0.07, 0.69,  35),
    ("DIY Dekor Kamar Aesthetic",             "Lifestyle",   16,  1.4, 0.92, 0.08, 0.73,  22),
    ("Berita Olahraga Premier League",        "Berita",       5,  1.1, 0.88, 0.09, 0.62,   1),
]


def build_videos_df():
    cols = ["judul", "kategori", "durasi_menit", "views_juta",
            "like_ratio", "ctr", "watch_completion", "freshness_hari"]
    df = pd.DataFrame(VIDEOS, columns=cols)
    df["id"] = range(len(df))
    return df


# ========== UTILITAS COSINE SIMILARITY ==========

def cosine_sim(a, b):
    """Cosine similarity untuk dua vektor numpy."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def cosine_sim_matrix(X):
    """Cosine similarity matrix N x N untuk array N x D."""
    X = np.asarray(X, dtype=float)
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1e-9, norms)
    X_norm = X / norms
    return X_norm @ X_norm.T
