import requests
import time
import json

def clean_price(price_data):
    """Professional cleaning for stringified API data."""
    try:
        # If the API sends a string like '["0.50", "0.50"]'
        if isinstance(price_data, str):
            price_data = json.loads(price_data)
        return [float(p) for p in price_data]
    except Exception:
        return [0.0, 0.0]

def quant_analysis():
    URL = "https://gamma-api.polymarket.com/markets?active=true&limit=10&order=volume24hr&dir=desc"
    
    try:
        response = requests.get(URL)
        markets = response.json()
        
        print(f"\n================ QUANT RECON: {time.ctime()} ================")
        print(f"{'MARKET NAME':<40} | {'SPREAD':<8} | {'EST. DAILY PROFIT'}")
        print("-" * 75)
        
        for m in markets:
            name = m.get('question', 'Unknown')[:38]
            
            # Use our new cleaner to handle those brackets
            prices = clean_price(m.get('outcomePrices'))
            
            if len(prices) >= 2:
                yes, no = prices[0], prices[1]
                # Spread Math: The gap between the two outcomes
                spread_pct = abs(1.0 - (yes + no)) * 100
                
                volume_24h = float(m.get('volume24hr', 0))
                # PM calculation: 1% market capture * current spread
                est_profit = (volume_24h * 0.01) * (spread_pct / 100)
                
                print(f"{name:<40} | {spread_pct:>7.2f}% | £{est_profit:>8.2f}")
            
    except Exception as e:
        print(f"DIAGNOSTIC: Data structure changed. CTO reviewing... ({e})")

if __name__ == "__main__":
    while True:
        quant_analysis()
        time.sleep(30)
if __name__ == "__main__":
    while True:
        quant_analysis()
        time.sleep(30) # High-frequency refresh for 2026 standards
