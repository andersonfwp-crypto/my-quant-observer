import requests
import time
import json

# CTO ARCHITECTURE: 2026 QUANT OBSERVER (V5)
# This version targets the Central Limit Order Book (CLOB) directly.

def get_market_data():
    # Primary CLOB Endpoint for 2026 Live Markets
    CLOB_URL = "https://clob.polymarket.com/markets"
    
    try:
        # Fetching live order book metadata
        response = requests.get(CLOB_URL, timeout=10)
        markets = response.json()
        
        print(f"\n🏛️  QUANT COMMAND CENTER: {time.ctime()}")
        print(f"{'MARKET TARGET':<35} | {'VOL (24H)':<10} | {'REBATE EDGE'}")
        print("-" * 75)
        
        # We look for the top 12 most active markets for our £5,000 deployment
        count = 0
        for m in markets:
            if count >= 12: break
            
            # Extracting the question name
            name = m.get('description', 'Niche Event')[:33]
            
            # In 2026, 'volume' is often nested or listed as a string
            raw_vol = m.get('volume', 0)
            try:
                vol_24h = float(raw_vol)
            except:
                vol_24h = 0.0
                
            # STRATEGY: Maker Rebate Capture
            # To hit £5k/month, we need £167/day.
            # Calculation: (Our Capital * Volume Capture * Rebate Rate)
            # 0.25% is the standard 2026 Maker Rebate.
            daily_profit = (vol_24h * 0.005) * 0.0025 # Estimating 0.5% market share
            
            # ALERTS: Trigger "Fire" if Daily Edge > £100
            status = "🔥" if daily_profit > 100 else "  "
            
            # Only display if there is actual activity
            if vol_24h > 500:
                print(f"{status}{name:<33} | ${vol_24h:>8,.0f} | £{daily_profit:>8.2f}")
                count += 1
                
        if count == 0:
            print(">> STATUS: Market scanning... (Waiting for High-Vol signals)")

    except Exception as e:
        print(f"CRITICAL CTO ALERT: Data Stream Interrupted. Reason: {e}")

if __name__ == "__main__":
    while True:
        get_market_data()
        time.sleep(20) # 20s interval to prevent API 'Rate Limiting'

if __name__ == "__main__":
    while True:
        quant_recon_v3()
        time.sleep(15) # Refreshing every 15s to catch 2026 volatility
