import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# =========================
# SCRAPING + LIMPIEZA
# =========================
url = "https://en.wikipedia.org/wiki/List_of_most-streamed_songs_on_Spotify"
headers = {"User-Agent": "JL-WebScraping-Training/1.0 (educational project)"}

response = requests.get(url, headers=headers, timeout=30)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find_all("table", class_="wikitable")[0]
rows = table.find_all("tr")

data = []
for row in rows[1:]:
    cells = row.find_all(["th", "td"])
    cell_texts = [c.get_text(" ", strip=True) for c in cells]
    if len(cell_texts) == 6:
        data.append(cell_texts)

columns = ["rank", "song", "artist", "streams_billions", "release_date", "ref"]
df = pd.DataFrame(data, columns=columns)

df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
df["song"] = df["song"].str.replace('"', "", regex=False).str.strip()
df["artist"] = df["artist"].str.replace(r"\s+", " ", regex=True).str.strip()
df["streams_billions"] = pd.to_numeric(df["streams_billions"], errors="coerce")
df = df.dropna(subset=["streams_billions"]).copy()

# =========================
# VISUALIZACIÓN 1
# =========================

top10 = df.sort_values("streams_billions", ascending=False).head(10)

plt.figure()
plt.barh(top10["song"], top10["streams_billions"])
plt.xlabel("Streams (billions)")
plt.ylabel("Song")
plt.title("Top 10 canciones más reproducidas en Spotify")
plt.gca().invert_yaxis()  # la más escuchada arriba
plt.tight_layout()
plt.savefig("assets/top10_songs.png")
print("Gráfico guardado en assets/top10_songs.png")











