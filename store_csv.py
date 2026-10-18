import pandas as pd
from pathlib import Path

RAW_FILE = Path("lake/raw/csv/traffic/store_traffic.csv")
SILVER_FILE = Path("lake/silver/csv/store_traffic.parquet")

SILVER_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_FILE)

df["date"] = pd.to_datetime(df["date"])
df["visitor_count"] = df["visitor_count"].astype(int)

df.drop_duplicates(inplace=True)

df.to_parquet(
    SILVER_FILE,
    index=False,
    engine="pyarrow"
)

print(f"Success: {SILVER_FILE}")