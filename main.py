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

import requests
import time
import json

def quant_recon_v3():
    # 2026 Gamma API - focus on high-frequency crypto/sports
    URL = "https://gamma-api.polymarket.com/markets?active=true&limit=15&order=volume24hr&dir=desc"
    
    try:
        response = requests.get(URL)
        markets = response.json()
        
        print(f"\n======== HEDGE FUND RECON: {time.ctime()} ========")
        print(f"{'TARGET MARKET':<35} | {'SPREAD':<6} | {'REBATE+'} | {'DAILY EDGE'}")
        print("-" * 80)
        
        for m in markets:
            name = m.get('question', 'Unknown')[:33]
            prices = m.get('outcomePrices', [0, 0])
            
            # Sanitizing data
            if isinstance(prices, str): prices = json.loads(prices)
            yes, no = float(prices[0]), float(prices[1])
            
            # In 2026, many markets have a 1% 'Taker Fee' that goes to US (the Makers)
            spread_pct = abs(1.0 - (yes + no)) * 100
            rebate_rate = 0.0025 # Standard 0.25% Maker Rebate in Jan 2026
            
            volume = float(m.get('volume24hr', 0))
            
            # Scaled Profit: (Spread + Rebate) * (Our 1% share of total daily volume)
            daily_edge = (volume * 0.01) * ((spread_pct / 100) + rebate_rate)
            
            # Highlight high-potential targets
            indicator = "🔥" if daily_edge > 100 else "  "
            print(f"{indicator}{name:<33} | {spread_pct:>5.1f}% | 0.25%   | £{daily_edge:>8.2f}")
            
    except Exception as e:
        print(f"RECON PAUSED: {e}")

if __name__ == "__main__":
    while True:
        quant_recon_v3()
        time.sleep(15) # Refreshing every 15s to catch 2026 volatility
