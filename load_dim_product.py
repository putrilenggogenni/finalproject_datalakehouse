import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# source
conn_source = psycopg2.connect(
    host="localhost",
    database="staging_db",
    user="postgres",
    password="password"
)

# destination
engine_dw = create_engine(
    "postgresql://postgres:password@localhost/adventureworks_dw"
)

query = """
SELECT
    p.productid,
    p.name AS product_name,
    ps.name AS subcategory,
    pc.name AS category,
    p.color,
    p.listprice
FROM production.product p
LEFT JOIN production.productsubcategory ps
    ON p.productsubcategoryid = ps.productsubcategoryid
LEFT JOIN production.productcategory pc
    ON ps.productcategoryid = pc.productcategoryid
"""

df = pd.read_sql(query, conn_source)

df.to_sql(
    "dim_product",
    engine_dw,
    schema="dw",
    if_exists="append",
    index=False
)

print("dim_product loaded")