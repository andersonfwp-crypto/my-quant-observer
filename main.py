import requests
import time
import os

def get_market_data():
    # Public endpoint for Polymarket 2026 data
    URL = "https://gamma-api.polymarket.com/markets?active=true&limit=5"
    try:
        response = requests.get(URL)
        markets = response.json()
        print(f"\n--- QUANT OBSERVER REPORT: {time.ctime()} ---")
        for m in markets:
            name = m.get('question', 'Unknown')
            # In 2026, prices are represented as 0.0 to 1.0
            yes_price = float(m.get('outcomePrices', [0,0])[0])
            no_price = float(m.get('outcomePrices', [0,0])[1])
            spread = 1.0 - (yes_price + no_price)
            
            print(f"MARKET: {name[:50]}...")
            print(f"  > Yes: {yes_price:.2f} | No: {no_price:.2f}")
            print(f"  > Available Spread: {abs(spread)*100:.2f}%")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    while True:
        get_market_data()
        time.sleep(60) # Watch the market every minute
