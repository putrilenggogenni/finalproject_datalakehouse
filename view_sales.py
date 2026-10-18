import pandas as pd
from pathlib import Path

INPUT_FILE = Path("lake/silver/excel/sales_offline.parquet")
OUTPUT_FILE = Path("lake/gold/sales/sales_mart.parquet")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(INPUT_FILE)

df["sales_amount"] = (
    df["orderqty"] *
    df["unitprice"]
)

df.to_parquet(
    OUTPUT_FILE,
    index=False
)
print(df.columns)
print("Sales Gold Created")