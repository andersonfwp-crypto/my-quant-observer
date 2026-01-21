import requests
import time

# CTO ARCHITECTURE: 2026 STABILITY UPGRADE (V8)
# This version uses Gamma Endpoints for higher uptime and diagnostic reporting.

def diagnostic_hunt():
    # Switching to Gamma API - Generally more stable for public 'Recon'
    URL = "https://gamma-api.polymarket.com/markets?active=true&limit=20&order=volume24hr&dir=desc"
    
    try:
        # Step 1: Check if the exchange even sees us
        geo_check = requests.get("https://polymarket.com/api/geoblock", timeout=5).json()
        location = geo_check.get('country', 'Unknown')
        is_blocked = geo_check.get('blocked', False)
        
        print(f"\n🌍 SERVER LOCATION: {location} | BLOCKED: {is_blocked}")
        print(f"📊  STABILITY RECON: {time.ctime()}")
        print(f"{'MARKET NAME':<35} | {'VOL (24H)':<10} | {'DAILY EDGE'}")
        print("-" * 75)
        
        response = requests.get(URL, timeout=15)
        markets = response.json()
        
        count = 0
        for m in markets:
            name = m.get('question', 'Unknown')[:33]
            vol_24h = float(m.get('volume24hr', 0) or 0)
            
            # Math: 0.25% Rebate * 1% Volume Capture
            daily_edge = (vol_24h * 0.01) * 0.0025
            
            if vol_24h > 100:
                status = "🔥" if daily_edge > 100 else "  "
                print(f"{status}{name:<33} | ${vol_24h:>8,.0f} | £{daily_edge:>8.2f}")
                count += 1
            if count >= 10: break

        if count == 0:
            print(">> ALERT: Connection active, but no high-volume markets found.")

    except Exception as e:
        print(f"CONNECTION ERROR: {e}")

if __name__ == "__main__":
    while True:
        diagnostic_hunt()
        time.sleep(60) # Slower heartbeat to avoid 'Rate Limiting'
