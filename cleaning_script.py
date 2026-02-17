import pandas as pd
import numpy as np
from datetime import datetime

# Load dataset
df = pd.read_csv("C:\\Users\\tasne\\Downloads\\titles.csv")

original_shape = df.shape

# -------------------------------
# 1. Drop row with missing title
# -------------------------------
df = df.dropna(subset=["title"])

# -------------------------------
# 2. Fill categorical missing values
# -------------------------------
df["age_certification"] = df["age_certification"].fillna("Unknown")
df["description"] = df["description"].fillna("No description")
df["imdb_id"] = df["imdb_id"].fillna("Not Available")

# -------------------------------
# 3. Handle seasons column
# If type is Movie → seasons = 0
# -------------------------------
df.loc[df["type"] == "MOVIE", "seasons"] = 0
df["seasons"] = df["seasons"].fillna(0)

# -------------------------------
# 4. Fill numeric missing values with median
# -------------------------------
numeric_cols = ["imdb_score", "imdb_votes", "tmdb_score", "tmdb_popularity"]

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# -------------------------------
# 5. Convert data types properly
# -------------------------------
df["release_year"] = df["release_year"].astype(int)
df["imdb_votes"] = df["imdb_votes"].astype(int)
df["seasons"] = df["seasons"].astype(int)

# -------------------------------
# 6. Feature Engineering
# -------------------------------
current_year = datetime.now().year
df["content_age"] = current_year - df["release_year"]

df["average_score"] = (df["imdb_score"] + df["tmdb_score"]) / 2

# -------------------------------
# 7. Clean Genres & Countries
# -------------------------------
df["genres"] = df["genres"].str.replace("[", "", regex=False)\
                           .str.replace("]", "", regex=False)\
                           .str.replace("'", "", regex=False)\
                           .str.lower()

df["production_countries"] = df["production_countries"].str.replace("[", "", regex=False)\
                                                         .str.replace("]", "", regex=False)\
                                                         .str.replace("'", "", regex=False)\
                                                         .str.lower()

# -------------------------------
# 8. Remove duplicates
# -------------------------------
df = df.drop_duplicates()

# -------------------------------
# 9. Save cleaned dataset
# -------------------------------
df.to_csv("cleaned_netflix.csv", index=False)

# -------------------------------
# 10. Create Cleaning Log
# -------------------------------
with open("cleaning_log.txt", "w") as log:
    log.write("NETFLIX DATA CLEANING REPORT\n")
    log.write("-----------------------------\n")
    log.write(f"Original Shape: {original_shape}\n")
    log.write(f"Cleaned Shape: {df.shape}\n")
    log.write("\nMissing Values After Cleaning:\n")
    log.write(str(df.isnull().sum()))

print("Advanced Cleaning Completed Successfully!")
