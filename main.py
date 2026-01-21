import requests
import time

# CTO ARCHITECTURE: 2026 VOLUME MAGNET (V15)
# Filters out "Ghost Markets" and targets high-churn 'Lighter' and 'AI' assets.

def volume_magnet_scan():
    try:
        # Step 1: Identity Check
        geo = requests.get("https://polymarket.com/api/geoblock", timeout=5).json()
        print(f"\n🌍 HUB: {geo.get('country')} | BLOCKED: {geo.get('blocked')}")
        
        # Step 2: High-Volume Discovery (The 2026 'Whale' List)
        # We increase the limit to 100 to find the actual active needles in the haystack
        url = "https://gamma-api.polymarket.com/markets?active=true&limit=100&order=volume24hr&dir=desc"
        markets = requests.get(url, timeout=10).json()
        
        print(f"📡  ACTIVE CHURN MONITOR: {time.ctime()}")
        print(f"{'MARKET TARGET':<35} | {'PRICE':<7} | {'SPREAD':<7} | {'DAILY EDGE'}")
        print("-" * 85)

        count = 0
        for m in markets:
            if count >= 8: break
            
            name = m.get('question', 'Unknown')[:33]
            prices = m.get('outcomePrices', [0, 0])
            
            # Clean price parsing
            yes_price = float(prices[0] if prices else 0)
            no_price = float(prices[1] if len(prices) > 1 else 0)
            spread = abs(1.0 - (yes_price + no_price))
            
            # THE FILTER: Only trade if the market is competitive
            # We want markets where the outcome is uncertain (Price between 0.10 and 0.90)
            if 0.10 < yes_price < 0.90 and spread < 0.05:
                vol_24h = float(m.get('volume24hr', 0) or 0)
                
                # Math: Our share of the daily churn
                daily_edge = (vol_24h * 0.001) * 0.0025 
                
                fire = "🔥" if vol_24h > 1000000 else "  "
                print(f"{fire}{name:<33} | ${yes_price:<6.2f} | {spread*100:>5.1f}% | £{daily_edge:>8.2f}")
                count += 1

    except Exception as e:
        print(f"RECOVERY: {e}")

if __name__ == "__main__":
    while True:
        volume_magnet_scan()
        time.sleep(30)
