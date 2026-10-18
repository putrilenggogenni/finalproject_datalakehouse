import json
import pandas as pd
from pathlib import Path

RAW_DIR = Path("lake/raw/json/twitter")
SILVER_FILE = Path("lake/silver/json/twitter.parquet")

SILVER_FILE.parent.mkdir(parents=True, exist_ok=True)

all_data = []

for file in RAW_DIR.glob("twitter_day_*.json"):

    with open(file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    df = pd.json_normalize(
        json_data["data"],
        sep="_"
    )

    all_data.append(df)

twitter_df = pd.concat(
    all_data,
    ignore_index=True
)

twitter_df["created_at"] = pd.to_datetime(
    twitter_df["created_at"]
)

twitter_df.drop_duplicates(
    subset=["id"],
    inplace=True
)

twitter_df.to_parquet(
    SILVER_FILE,
    index=False,
    engine="pyarrow"
)

print(f"Success: {SILVER_FILE}")
print(f"Total Tweets: {len(twitter_df)}")