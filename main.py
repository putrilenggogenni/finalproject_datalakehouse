import os

folders = [
    "lake/raw/excel",
    "lake/raw/json/twitter",
    "lake/raw/csv/traffic",

    "lake/silver/excel",
    "lake/silver/json",
    "lake/silver/csv",

    "lake/gold/sales",
    "lake/gold/twitter",
    "lake/gold/traffic",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("✅ Folder lakehouse berhasil dibuat")