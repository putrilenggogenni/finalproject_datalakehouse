import pandas as pd
import psycopg2

# =====================
# CONFIG
# =====================

PARQUET_FILE = "lake/gold/twitter/tweet_sentiment.parquet"

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

print(df.columns.tolist())

# =====================
# DATE KEY
# =====================

df["date_key"] = (
    pd.to_datetime(df["created_at"])
      .dt.strftime("%Y%m%d")
      .astype(int)
)

# =====================
# SENTIMENT MAPPING
# =====================

sentiment_map = {
    "Positive": 1,
    "Neutral": 2,
    "Negative": 3
}

df["sentiment_key"] = (
    df["sentiment"]
    .map(sentiment_map)
)

# =====================
# SCORE
# =====================

df["positive_score"] = (
    df["sentiment"]
    .apply(lambda x: 1 if x == "Positive" else 0)
)

df["negative_score"] = (
    df["sentiment"]
    .apply(lambda x: 1 if x == "Negative" else 0)
)

# =====================
# LOAD DIM PRODUCT
# =====================

dim_product = pd.read_sql(
    """
    SELECT
        product_key,
        product_name
    FROM dw.dim_product
    """,
    conn
)

df = df.merge(
    dim_product,
    on="product_name",
    how="left"
)

# =====================
# INSERT FACT
# =====================

cursor = conn.cursor()

for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO dw.fact_twitter_sentiment
        (
            tweet_id,
            date_key,
            product_key,
            sentiment_key,
            positive_score,
            negative_score,
            like_count,
            reply_count,
            retweet_count,
            quote_count
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """,
        (
            row["id"],
            row["date_key"],
            row["product_key"],
            row["sentiment_key"],
            row["positive_score"],
            row["negative_score"],
            row["like_count"],
            row["reply_count"],
            row["retweet_count"],
            row["quote_count"]
        )
    )

conn.commit()

cursor.close()
conn.close()

print("FACT TWITTER SENTIMENT LOADED")