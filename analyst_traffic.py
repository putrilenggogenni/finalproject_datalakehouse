import pandas as pd
import psycopg2

# =====================
# CONFIG
# =====================

PARQUET_FILE = "lake/gold/traffic/traffic_summary.parquet"

conn = psycopg2.connect(
    host="localhost",
    database="adventureworks_dw",
    user="postgres",
    password="password"
)

# =====================
# LOAD GOLD DATA
# =====================

df = pd.read_parquet(PARQUET_FILE)

# =====================
# DATE KEY
# =====================

df["date_key"] = (
    pd.to_datetime(df["date"])
      .dt.strftime("%Y%m%d")
      .astype(int)
)

# =====================
# LOAD DIM STORE
# =====================

dim_store = pd.read_sql(
    """
    SELECT store_key, store_id
    FROM dw.dim_store
    """,
    conn
)

df = df.merge(
    dim_store,
    on="store_id",
    how="left"
)

# =====================
# INSERT FACT
# =====================

cursor = conn.cursor()

for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO dw.fact_store_traffic
        (
            date_key,
            store_key,
            visitor_count
        )
        VALUES
        (
            %s,%s,%s
        )
        """,
        (
            row["date_key"],
            row["store_key"],
            row["visitor_count"]
        )
    )

conn.commit()

cursor.close()
conn.close()

print("FACT STORE TRAFFIC LOADED")