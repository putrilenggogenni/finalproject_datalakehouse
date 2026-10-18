import pandas as pd
import random
import os

# folder raw
path = "lake/raw/csv/traffic/"
os.makedirs(path, exist_ok=True)

stores = {
    "STORE01": (180, 300),
    "STORE02": (140, 260),
    "STORE03": (60, 160),
    "STORE04": (100, 220),
    "STORE05": (80, 260),
}

rows = []

for day in range(1, 31):
    date = f"2025-01-{day:02d}"

    for store, (low, high) in stores.items():
        visitor = random.randint(low, high)
        rows.append([date, store, visitor])

df = pd.DataFrame(rows, columns=["date","store_id","visitor_count"])

file_path = path + "store_traffic.csv"

df.to_csv(file_path, index=False)

print("INGEST3 DONE →", file_path)