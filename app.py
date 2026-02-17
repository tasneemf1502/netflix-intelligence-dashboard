import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Netflix Intelligence Dashboard", layout="wide")

# ---------------- POSTER GENERATOR ----------------
def generate_poster(title):
    title = title.replace(" ", "+")
    return f"https://via.placeholder.com/300x450/000000/E50914?text={title}"

# ---------------- NETFLIX PREMIUM STYLE ----------------
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
.main { background-color: #0e1117; }

h1, h2, h3 {
    color: #E50914;
}

/* Poster Card */
.poster-card {
    position: relative;
    border-radius: 15px;
    overflow: hidden;
    transition: transform 0.3s ease;
}

.poster-card:hover {
    transform: scale(1.05);
}

/* Rating Badge */
.rating-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: #E50914;
    color: white;
    padding: 5px 8px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: bold;
}

.poster-title {
    text-align: center;
    font-size: 14px;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Netflix Premium Intelligence Dashboard")
st.markdown("AI-Powered Content Insights & Recommendation Engine")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_netflix.csv")

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔎 Filter Content")
selected_type = st.sidebar.selectbox("Select Type", df["type"].unique())

filtered_df = df[df["type"] == selected_type]

# ---------------- METRICS ----------------
st.header("📊 Platform Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", filtered_df.shape[0])
col2.metric("Avg IMDb", round(filtered_df["imdb_score"].mean(), 2))
col3.metric("Top IMDb", round(filtered_df["imdb_score"].max(), 1))

# ---------------- TOP 10 POSTER GRID ----------------
st.header("🔥 Top 10 Highest Rated")

top_rated = filtered_df.sort_values(by="imdb_score", ascending=False).head(10)

cols = st.columns(5)

for i, (_, row) in enumerate(top_rated.iterrows()):
    with cols[i % 5]:
        poster_url = generate_poster(row["title"])
        st.markdown(f"""
        <div class="poster-card">
            <img src="{poster_url}" style="width:100%; border-radius:15px;">
            <div class="rating-badge">⭐ {row['imdb_score']}</div>
        </div>
        <div class="poster-title">{row['title']}</div>
        """, unsafe_allow_html=True)

# ---------------- RECOMMENDATION ENGINE ----------------
st.header("🤖 Smart Recommendation Engine")

movie_list = filtered_df["title"].dropna().unique()
selected_movie = st.selectbox("Choose a title", movie_list)

if selected_movie:

    selected_row = filtered_df[filtered_df["title"] == selected_movie].iloc[0]

    genre = selected_row["genres"]
    imdb_score = selected_row["imdb_score"]

    recommendations = filtered_df[
        (filtered_df["genres"] == genre) &
        (filtered_df["title"] != selected_movie) &
        (abs(filtered_df["imdb_score"] - imdb_score) <= 1)
    ].sort_values(by="imdb_score", ascending=False).head(5)

    st.subheader("🎯 Recommended For You")

    if recommendations.empty:
        st.warning("No close matches found. Try another title.")
    else:
        rec_cols = st.columns(5)
        for i, (_, row) in enumerate(recommendations.iterrows()):
            with rec_cols[i % 5]:
                poster_url = generate_poster(row["title"])
                st.markdown(f"""
                <div class="poster-card">
                    <img src="{poster_url}" style="width:100%; border-radius:15px;">
                    <div class="rating-badge">⭐ {row['imdb_score']}</div>
                </div>
                <div class="poster-title">{row['title']}</div>
                """, unsafe_allow_html=True)

# ---------------- TREND CHART ----------------
st.header("📅 Content Growth Over Time")

year_counts = filtered_df["release_year"].value_counts().sort_index()
st.line_chart(year_counts)

# ---------------- DOWNLOAD ----------------
st.download_button(
    label="⬇ Download Filtered Dataset",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_netflix_data.csv",
    mime="text/csv"
)
