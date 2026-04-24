from database import get_db_connection
from utils.logger import log_info, log_error


import requests

def search_items(query):
    try:
        response = requests.get("https://dummyjson.com/products")
        data = response.json()
    
        products = data.get("products", [])
        results = []

        for item in products:
            title = item["title"].lower()

            if query.lower() in title:
                results.append({
                    "name": item["title"],
                    "price": item["price"],
                    "sold": 100
                })

        # ✅ fallback if no matches
        if not results:
            for item in products:
                results.append({
                    "name": item["title"],
                    "price": item["price"],
                    "sold": 100
                })

        return results

    except Exception as e:
        log_error(str(e))
        return []


def calculate_profit(buy_price, sell_price, shipping):
    ebay_fee_rate = 0.13
    fee = sell_price * ebay_fee_rate
    profit = sell_price - buy_price - shipping - fee

    return {
        "buy_price": buy_price,
        "sell_price": sell_price,
        "shipping": shipping,
        "fee": round(fee, 2),
        "profit": round(profit, 2),
    }


def save_items_to_db(items):
    conn = get_db_connection()
    cursor = conn.cursor()

    for item in items:
        cursor.execute(
            "INSERT INTO items (name, price, sold) VALUES (?, ?, ?)",
            (
                item.get("name", "Unknown"),
                item.get("price", 0),
                item.get("sold", 0),
            ),
        )

    conn.commit()
    conn.close()


def analyze_items(query, buy_price_estimate):
    items = search_items(query)  # later we make this dynamic
    save_items_to_db(items)

    results = []

    for item in items:
        sell_price = item["price"]
        shipping = 5
        ebay_fee_rate = 0.13
        fee = sell_price * ebay_fee_rate
        profit = sell_price - buy_price_estimate - shipping - fee

        results.append(
            {
                "name": item["name"],
                "sell_price": sell_price,
                "estimated_profit": round(profit, 2),
                "sold_volume": item.get("sold", 0),
            }
        )

    # sort best profit first
    results.sort(key=lambda x: x["estimated_profit"], reverse=True)
    return results


def get_trending_items():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, COUNT(*) as frequency
        FROM items
        GROUP BY name
        ORDER BY frequency DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    results = []

    for row in rows:
        results.append(
            {
                "name": row["name"],
                "frequency": row["frequency"],
            }
        )

    return results


def get_smart_trending(buy_price):
    try:
        log_info("Smart trending function called")
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, AVG(price) as avg_price, SUM(sold) as total_sold, COUNT(*) as frequency
            FROM items
            GROUP BY name
        """)

        rows = cursor.fetchall()
        conn.close()

        results = []

        for row in rows:
            log_info(f"Processing item: {row['name']}")
            sell_price = row["avg_price"]
            total_sold = row["total_sold"]

            ebay_fee = sell_price * 0.13
            shipping = 5
            profit = sell_price - buy_price - ebay_fee - shipping

            score = profit * total_sold

            results.append(
                {
                    "name": row["name"],
                    "avg_price": round(sell_price, 2),
                    "total_sold": total_sold,
                    "estimated_profit": round(profit, 2),
                    "score": round(score, 2),
                }
            )

        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    except Exception as e:
        log_error(str(e))
        return []
