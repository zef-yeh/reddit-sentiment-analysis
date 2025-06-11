import pandas as pd
import sqlite3
import os

CSV_PATH = "electronics_product.csv"  # dataset name, using KAGGLE can replace with any .csv
DB_PATH = "reddit_bifl.db"

def normalize(name):
    return ' '.join(name.lower().strip().split())

df = pd.read_csv(CSV_PATH)
df = df[df["name"].notna()]
unique_products = set(normalize(p) for p in df["name"].unique())

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS catalog (product_normalized TEXT PRIMARY KEY)")
cursor.executemany("INSERT OR IGNORE INTO catalog VALUES (?)", [(p,) for p in unique_products])
conn.commit()
conn.close()
print(f"Loaded {len(unique_products)} products into catalog.")
