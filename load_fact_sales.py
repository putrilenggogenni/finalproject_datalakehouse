import pandas as pd
from sqlalchemy import create_engine

# =====================================================
# CONNECTION
# =====================================================

SOURCE_DB = create_engine(
    "postgresql+psycopg2://postgres:password@localhost/staging_db"
)

DW_DB = create_engine(
    "postgresql+psycopg2://postgres:password@localhost/adventureworks_dw"
)

# =====================================================
# EXTRACT ONLINE SALES
# =====================================================

query_sales = """
SELECT
    h.salesorderid,
    h.orderdate,
    h.customerid,
    d.productid,
    d.orderqty,
    d.unitprice,
    d.unitpricediscount,
    (
        d.orderqty *
        d.unitprice *
        (1 - d.unitpricediscount)
    ) AS sales_amount
FROM sales.salesorderheader h
JOIN sales.salesorderdetail d
    ON h.salesorderid = d.salesorderid
WHERE h.onlineorderflag = TRUE
"""

sales_df = pd.read_sql(query_sales, SOURCE_DB)

print(f"Sales rows : {len(sales_df)}")

# =====================================================
# DIM PRODUCT
# =====================================================

dim_product = pd.read_sql(
    """
    SELECT
        product_key,
        productid
    FROM dw.dim_product
    """,
    DW_DB
)

# =====================================================
# DIM CUSTOMER
# =====================================================

dim_customer = pd.read_sql(
    """
    SELECT
        customer_key,
        customerid
    FROM dw.dim_customer
    """,
    DW_DB
)

# =====================================================
# MAPPING
# =====================================================

sales_df = sales_df.merge(
    dim_product,
    on="productid",
    how="left"
)

sales_df = sales_df.merge(
    dim_customer,
    on="customerid",
    how="left"
)

# =====================================================
# DATE KEY
# =====================================================

sales_df["date_key"] = (
    pd.to_datetime(sales_df["orderdate"])
    .dt.strftime("%Y%m%d")
    .astype(int)
)

# =====================================================
# CHANNEL
# =====================================================

sales_df["channel"] = "Online"

# =====================================================
# FINAL FACT
# =====================================================

fact_sales = sales_df[
    [
        "salesorderid",
        "date_key",
        "product_key",
        "customer_key",
        "channel",
        "orderqty",
        "unitprice",
        "unitpricediscount",
        "sales_amount"
    ]
].copy()

fact_sales.rename(
    columns={
        "unitpricediscount": "discount"
    },
    inplace=True
)

# =====================================================
# LOAD FACT
# =====================================================

fact_sales.to_sql(
    "fact_sales",
    DW_DB,
    schema="dw",
    if_exists="append",
    index=False
)

print(f"{len(fact_sales)} rows inserted to fact_sales")