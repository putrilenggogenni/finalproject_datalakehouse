import pandas as pd
import psycopg2
from sqlalchemy import create_engine

conn_source = psycopg2.connect(
    host="localhost",
    database="staging_db",
    user="postgres",
    password="password"
)

engine_dw = create_engine(
    "postgresql://postgres:@localhost/adventureworks_dw"
)

query = """
SELECT
    c.customerid,
    c.territoryid,
    st.name AS territory_name,
    st.countryregioncode,
    st."group" AS territory_group
FROM sales.customer c
LEFT JOIN sales.salesterritory st
    ON c.territoryid = st.territoryid
"""

df = pd.read_sql(query, conn_source)

df.to_sql(
    "dim_customer",
    engine_dw,
    schema="dw",
    if_exists="append",
    index=False
)

print("dim_customer loaded")