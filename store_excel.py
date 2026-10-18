import pandas as pd
from pathlib import Path

RAW_FILE = Path("lake/raw/excel/sales_offline.xlsx")
SILVER_FILE = Path("lake/silver/excel/sales_offline.parquet")

SILVER_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(RAW_FILE)

df.drop_duplicates(inplace=True)

df.to_parquet(
    SILVER_FILE,
    index=False,
    engine="pyarrow"
)

print(f"Success: {SILVER_FILE}")