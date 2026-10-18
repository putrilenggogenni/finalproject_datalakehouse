import pandas as pd
import psycopg2

# =========================
# CONFIG
# =========================

PARQUET_FILE = "lake/gold/sales/sales_mart.parquet"

conn = psycopg2.connect(
    host="localhost",
    database="adventureworks_dw",
    user="postgres",
    password="password"
)

# =========================
# LOAD DATA
# =========================

df = pd.read_parquet(PARQUET_FILE)

# date_key
df["date_key"] = pd.to_datetime(
    df["orderdate"]
).dt.strftime("%Y%m%d").astype(int)

# =========================
# LOAD DIMENSIONS
# =========================

dim_product = pd.read_sql(
    """
    SELECT product_key, productid
    FROM dw.dim_product
    """,
    conn
)

dim_customer = pd.read_sql(
    """
    SELECT customer_key, customerid
    FROM dw.dim_customer
    """,
    conn
)

# =========================
# LOOKUP
# =========================

df = df.merge(
    dim_product,
    on="productid",
    how="left"
)

df = df.merge(
    dim_customer,
    on="customerid",
    how="left"
)

df["channel"] = "Offline"

# =========================
# INSERT FACT SALES
# =========================

cursor = conn.cursor()

for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO dw.fact_sales
        (
            salesorderid,
            date_key,
            product_key,
            customer_key,
            channel,
            orderqty,
            unitprice,
            discount,
            sales_amount
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """,
        (
            row["salesorderid"],
            row["date_key"],
            row["product_key"],
            row["customer_key"],
            row["channel"],
            row["orderqty"],
            row["unitprice"],
            row["unitpricediscount"],
            row["sales_amount"]
        )
    )

conn.commit()

cursor.close()
conn.close()

print("FACT SALES LOADED")