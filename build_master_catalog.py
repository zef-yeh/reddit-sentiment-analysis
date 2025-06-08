import pandas as pd
import sqlite3
import os

# ---- CONFIG ----
CSV_PATH = "electronics_product.csv"  # <-- replace with your actual file path
PRODUCT_COLUMN = "name"       # <-- adjust to match your dataset
DB_PATH = "reddit_bifl.db"

# ---- NORMALIZATION FUNCTION ----
def normalize(name):
    return ' '.join(name.lower().strip().split())

# ---- LOAD & PROCESS CSV ----
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")

df = pd.read_csv(CSV_PATH)

if PRODUCT_COLUMN not in df.columns:
    raise ValueError(f"Column '{PRODUCT_COLUMN}' not found in dataset")

unique_products = df[PRODUCT_COLUMN].dropna().unique()
normalized_products = set(normalize(name) for name in unique_products if isinstance(name, str) and len(name.strip()) > 3)

# ---- WRITE TO DATABASE ----
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS catalog (
    product_normalized TEXT PRIMARY KEY
)
''')

cursor.executemany('''
INSERT OR IGNORE INTO catalog (product_normalized) VALUES (?)
''', [(p,) for p in normalized_products])

conn.commit()
conn.close()

print(f"Catalog updated: {len(normalized_products)} products inserted into 'catalog' table.")
