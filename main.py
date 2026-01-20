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
import requests
import time

def quant_analysis():
    # Using the 2026 Gamma API for Polymarket
    URL = "https://gamma-api.polymarket.com/markets?active=true&limit=10&order=volume24hr&dir=desc"
    
    try:
        response = requests.get(URL)
        markets = response.json()
        
        print(f"\n================ QUANT RECON: {time.ctime()} ================")
        print(f"{'MARKET NAME':<40} | {'SPREAD':<8} | {'EST. DAILY PROFIT'}")
        print("-" * 75)
        
        for m in markets:
            name = m.get('question', 'Unknown')[:38]
            prices = m.get('outcomePrices', [0, 0])
            
            # Math: 1.0 - (Yes + No) = The "Gap" we capture as Market Makers
            yes, no = float(prices[0]), float(prices[1])
            spread_pct = (1.0 - (yes + no)) * 100
            
            # Volume helps us calculate how often our £5,000 would "turn over"
            volume_24h = float(m.get('volume24hr', 0))
            
            # Potential Daily Profit = (Our Capital * Spread * Turnovers)
            # Assuming we capture 1% of the daily volume with our £5,000
            est_profit = (volume_24h * 0.01) * (spread_pct / 100)
            
            print(f"{name:<40} | {spread_pct:>7.2f}% | £{est_profit:>8.2f}")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    while True:
        quant_analysis()
        time.sleep(30) # High-frequency refresh for 2026 standards
