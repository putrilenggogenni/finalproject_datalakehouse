import pandas as pd
from sqlalchemy import create_engine

# koneksi ke staging DB (yang sudah mirror AdventureWorks)
engine = create_engine(
    "postgresql://postgres:password@localhost/staging_db"
)

# ambil OFFLINE sales (onlineorderflag = false
query = """
SELECT 
    soh.salesorderid,
    soh.orderdate,
    soh.duedate,
    soh.shipdate,
    soh.status,
    soh.onlineorderflag,
    soh.customerid,
    soh.salespersonid,
    soh.territoryid,
    soh.subtotal,
    soh.taxamt,
    soh.freight,
    soh.totaldue,
    sod.productid,
    sod.orderqty,
    sod.unitprice,
    sod.unitpricediscount
FROM sales.salesorderheader soh
JOIN sales.salesorderdetail sod
    ON soh.salesorderid = sod.salesorderid
WHERE soh.onlineorderflag = false;
"""

# execute query
df = pd.read_sql(query, engine)

# optional: rapihin nama kolom (biar konsisten)
df.columns = [col.lower() for col in df.columns]

# output ke RAW Excel
output_path = "lake/raw/excel/sales_offline.xlsx"
df.to_excel(output_path, index=False)

print(f"SUCCESS: offline sales exported to {output_path}")