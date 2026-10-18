import json
import random
import os
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# PRODUCTS
# ─────────────────────────────────────────────

PRODUCTS = [
    "Adjustable Race",
    "Flat Washer 4",
    "Thin-Jam Hex Nut 16",
    "External Lock Washer 8",
    "Metal Sheet 2",
    "LL Road Frame - Black, 58",
    "Mountain-200 Black, 46",
    "Road-550-W Yellow, 38",
    "Headlights - Dual-Beam",
    "Men's Sports Shorts, L",
    "Classic Vest, M",
    "Women's Mountain Shorts, L",
    "Racing Socks, M",
    "Short-Sleeve Classic Jersey, S",
    "HL Touring Frame - Yellow, 46",
    "LL Mountain Frame - Silver, 40",
    "Touring-1000 Yellow, 46",
    "Mountain-500 Silver, 42",
    "Road-750 Black, 44",
]

# ─────────────────────────────────────────────
# OUTPUT CONFIG
# ─────────────────────────────────────────────

OUTPUT_DIR = "lake/raw/json/twitter/"
TOTAL_TWEETS = 1000
TOTAL_DAYS = 30
START_DATE = datetime(2025, 1, 1)

# ─────────────────────────────────────────────
# TEXT VARIATION LAYERS (INI KUNCINYA)
# ─────────────────────────────────────────────

PREFIX = [
    "", "tbh ", "ngl ", "honestly ", "imo ", "I think ",
]

EMOJI = [
    "", "🔥", "😤", "😍", "💀", "👍", "🤯"
]

TIME_HINT = [
    "", "after using it for days, ", "just got it and ", "after 1 week, "
]

POSITIVE = [
    "{product} is insane, way better than expected",
    "I love my {product}, quality is actually crazy good",
    "{product} feels premium and super solid",
    "no regrets buying {product}, worth every penny",
    "{product} exceeded my expectations by far",
]

NEUTRAL = [
    "{product} seems okay so far",
    "got {product}, will test it more",
    "{product} is average, nothing special yet",
    "using {product} right now, still evaluating",
]

NEGATIVE = [
    "{product} feels cheap, kinda disappointed",
    "not happy with {product}, expected better",
    "{product} broke too fast tbh",
    "regret buying {product}, not worth it",
]

WEIGHTED = (
    [(POSITIVE, 60)] +
    [(NEUTRAL, 25)] +
    [(NEGATIVE, 15)]
)

POOL = []
for group, w in WEIGHTED:
    POOL.extend([group] * w)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def generate_text(product):
    template = random.choice(random.choice(POOL))

    text = template.format(product=product)

    return (
        random.choice(PREFIX)
        + random.choice(TIME_HINT)
        + text
        + " "
        + random.choice(EMOJI)
    ).strip()


def metrics():
    return {
        "retweet_count": random.randint(0, 50),
        "reply_count": random.randint(0, 30),
        "like_count": random.randint(0, 200),
        "quote_count": random.randint(0, 20),
    }


def distribute(total, days):
    base, rem = divmod(total, days)
    arr = [base] * days
    for i in random.sample(range(days), rem):
        arr[i] += 1
    return arr

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    daily = distribute(TOTAL_TWEETS, TOTAL_DAYS)
    tweet_id = 3000000

    for day in range(TOTAL_DAYS):

        created_at = (START_DATE + timedelta(days=day)).isoformat() + "Z"
        count = daily[day]

        tweets = []

        for _ in range(count):

            product = random.choice(PRODUCTS)

            tweets.append({
                "id": str(tweet_id),
                "created_at": created_at,
                "author_id": str(random.randint(7000, 9000)),
                "username": f"user_{random.randint(7000, 9000)}",
                "text": generate_text(product),
                "lang": "en",
                "product_name": product,
                "public_metrics": metrics()
            })

            tweet_id += 1

        output = {"data": tweets}

        file_path = os.path.join(
            OUTPUT_DIR,
            f"twitter_day_{day+1}.json"
        )

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

        print(f"[✓] {file_path} → {count} tweets")

    print("\n✅ DONE FULL VARIATION PIPELINE")


if __name__ == "__main__":
    random.seed(42)
    main()