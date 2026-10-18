import pandas as pd
from pathlib import Path

INPUT_FILE = Path("lake/silver/csv/store_traffic.parquet")
OUTPUT_FILE = Path("lake/gold/traffic/traffic_summary.parquet")

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df = pd.read_parquet(INPUT_FILE)

def traffic_level(x):

    if x >= 220:
        return "High"

    elif x >= 120:
        return "Medium"

    return "Low"

df["traffic_level"] = (
    df["visitor_count"]
    .apply(traffic_level)
)

df.to_parquet(
    OUTPUT_FILE,
    index=False
)
print(df.columns)
print("Traffic Gold Created")