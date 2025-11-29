from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# ---------------- Selenium Setup ----------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

url = "https://www.imdb.com/chart/top/"
driver.get(url)
time.sleep(3)

# ---------------- Scraping ----------------
rows = driver.find_elements(By.CSS_SELECTOR, "ul.ipc-metadata-list li.ipc-metadata-list-summary-item")
print("Movies Found:", len(rows))

movie_data = []

for index, movie in enumerate(rows, start=1):
    try:
        title = movie.find_element(By.CSS_SELECTOR, ".ipc-title__text").text
        year = movie.find_element(By.CSS_SELECTOR, ".cli-title-metadata-item").text
        rating = movie.find_element(By.CSS_SELECTOR, ".ipc-rating-star--rating").text.split()[0]

        movie_data.append([index, title, year, rating])

    except Exception as e:
        print("Skipping movie due to error:", e)
        continue

driver.quit()

# ---------------- Save CSV ----------------
df = pd.DataFrame(movie_data, columns=["Rank", "Title", "Year", "IMDb Rating"])
df.to_csv("imdb_top_250_new.csv", index=False)

print("\nScraping Completed!")
print(f"Saved {len(df)} movies to imdb_top_250_new.csv")