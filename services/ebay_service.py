from database import get_db_connection
from utils.logger import log_info, log_error 

def search_items(query):
    return [  
        {"name": "Basketball Shoes", "price": 45, "sold": 120},	 
        {"name": "Running Shoes", "price": 60, "sold": 80},
        {"name": "Training Shoes", "price": 30, "sold": 200}
    ]


def calculate_profit(buy_price, sell_price, shipping):
    ebay_fee_rate = 0.13
    
    fee = sell_price * ebay_fee_rate 
    profit = sell_price - buy_price - shipping -fee

    return {
        "buy_price": buy_price,
        "sell_price": sell_price,
        "shipping": shipping, 
        "fee": round(fee, 2), 
        "profit": round(profit, 2)
    } 



def analyze_items(buy_price_estimate):
    items = search_items("shoes")   #later we make this dynamic
    save_items_to_db(items)

    results = []

    for item in items:
        sell_price = item["price"]
        shipping = 5   #simple estimate 

        ebay_fee_rate = 0.13
        fee = sell_price * ebay_fee_rate

        profit = sell_price - buy_price_estimate - shipping - fee

        results.append({
            "name": item.get("name", "Unknown Item"),
            "sell_price": sell_price,
            "estimated_profit": round(profit, 2),
            "sold_volume": item.get("sold", 0)
        })

       #sort best profit first 
        results.sort(key=lambda x: x["estimated_profit"], reverse=True)
 
        return results


from database import get_db_connection

def save_items_to_db(items):
    conn = get_db_connection()
    cursor = conn.cursor()

    for item in items:
        cursor.execute(
            "INSERT INTO items (name, price, sold) VALUES (?, ?, ?)", 
            ( 
                item.get("name", "Unknown"),
                item.get("price", 0), 
                item.get("sold", 0)
            ) 
        ) 
    
    conn.commit()
    conn.close() 


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
        results.append({ 
            "name": row["name"],
            "frequency": row["frequency"]
        })

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

        #calculate profit
            ebay_fee = sell_price * 0.13
            shipping = 5
            profit = sell_price - buy_price - ebay_fee - shipping

        #ranking score
            score = profit * total_sold

            results.append({
                "name": row["name"], 
                "avg_price": round(sell_price, 2), 
                "total_sold": total_sold, 
                "estimated_profit": round(profit, 2),
                "score": round(score, 2)
            })

        #sort best first
        results.sort(key=lambda x: x["score"], reverse=True)

        return results
    except Exception as e:
        log_error(str(e))
        raise
