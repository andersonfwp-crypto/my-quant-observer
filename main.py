import requests
import time

# CTO ARCHITECTURE: 2026 GLOBAL BYPASS (V9)
# Optimized for Amsterdam deployment to bypass US/UK Geoblocks.

def global_recon():
    # Sampling endpoint is the 'backdoor' for high-volume data in 2026
    URL = "https://clob.polymarket.com/sampling-simplified-markets"
    
    try:
        # Check our new identity
        geo = requests.get("https://polymarket.com/api/geoblock", timeout=5).json()
        print(f"\n🌍 IDENTITY: {geo.get('country', 'Unknown')} | BLOCKED: {geo.get('blocked')}")
        
        response = requests.get(URL, timeout=10)
        markets = response.json()
        
        print(f"📊  AMSTERDAM HUB RECON: {time.ctime()}")
        print(f"{'MARKET TARGET':<35} | {'PRICE':<8} | {'DAILY EDGE'}")
        print("-" * 75)
        
        count = 0
        for m in markets:
            # Only pull active markets with a valid price
            name = m.get('description', 'Unknown Event')[:33]
            price = float(m.get('last_trade_price', 0) or 0)
            
            # Since we are in Amsterdam, we can now see 'Liquidity'
            # Liquidity is the fuel for our £5,000/month engine
            liquidity = float(m.get('liquidity', 0) or 0)
            
            # MATH: Capturing 0.2% of the liquidity 'churn' daily
            daily_edge = (liquidity * 0.002) 
            
            if price > 0:
                status = "🔥" if daily_edge > 100 else "  "
                print(f"{status}{name:<33} | ${price:>6.2f} | £{daily_edge:>8.2f}")
                active_count = count + 1
                count += 1
            if count >= 12: break

        if count == 0:
            print(">> STATUS: Connection clear, but scanning for active ticks...")

    except Exception as e:
        print(f"ROUTING ERROR: {e} (Checking Amsterdam Tunnel...)")

if __name__ == "__main__":
    while True:
        global_recon()
        time.sleep(30)
