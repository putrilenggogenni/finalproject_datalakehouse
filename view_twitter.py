import pandas as pd
from pathlib import Path

INPUT_FILE = Path("lake/silver/json/twitter.parquet")

GOLD_DIR = Path("lake/gold/twitter")
GOLD_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(INPUT_FILE)

positive_words = [
    "good", "great", "excellent", "amazing",
    "love", "awesome", "perfect", "best",
    "satisfied", "recommended", "exceeded"
]

negative_words = [
    "bad", "poor", "terrible", "awful",
    "hate", "worst", "disappointed",
    "broken", "slow", "problem"
]

def sentiment(text):

    text = str(text).lower()

    pos = sum(word in text for word in positive_words)
    neg = sum(word in text for word in negative_words)

    if pos > neg:
        return "Positive"

    elif neg > pos:
        return "Negative"

    return "Neutral"


df["sentiment"] = df["text"].apply(sentiment)

# =================================
# TWEET SENTIMENT
# =================================

tweet_sentiment = df[
    [
        "id",
        "created_at",
        "product_name",
        "sentiment",
        "public_metrics_like_count",
        "public_metrics_reply_count",
        "public_metrics_retweet_count",
        "public_metrics_quote_count"
    ]
].copy()

tweet_sentiment.rename(
    columns={
        "public_metrics_like_count": "like_count",
        "public_metrics_reply_count": "reply_count",
        "public_metrics_retweet_count": "retweet_count",
        "public_metrics_quote_count": "quote_count"
    },
    inplace=True
)

tweet_sentiment.to_parquet(
    GOLD_DIR / "tweet_sentiment.parquet",
    index=False
)

# =================================
# PRODUCT REVIEW SUMMARY
# =================================

summary = (
    df.groupby(
        ["product_name", "sentiment"]
    )
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

summary.to_parquet(
    GOLD_DIR / "product_review_summary.parquet",
    index=False
)

# =================================
# PRODUCT RANKING
# =================================

ranking = (
    df[df["sentiment"] == "Positive"]
    .groupby("product_name")
    .size()
    .reset_index(name="total_positive")
    .sort_values(
        "total_positive",
        ascending=False
    )
)

ranking["rank"] = range(
    1,
    len(ranking) + 1
)

ranking.to_parquet(
    GOLD_DIR / "product_ranking.parquet",
    index=False
)

print("Twitter Gold Created")