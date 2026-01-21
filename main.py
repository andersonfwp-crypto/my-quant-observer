import requests
import time
import json

# CTO ARCHITECTURE: 2026 QUANT OBSERVER (V6 - AUTO-UNWRAPPER)
# Designed to handle nested CLOB API responses and schema shifts.

def get_market_data():
    # Primary 2026 CLOB Endpoint
    CLOB_URL = "https://clob.polymarket.com/markets"
    
    try:
        response = requests.get(CLOB_URL, timeout=10)
        raw_payload = response.json()
        
        # --- DATA UNWRAPPER LOGIC ---
        # The API often wraps the list in a dictionary key like 'data' or 'markets'
        markets = []
        if isinstance(raw_payload, list):
            markets = raw_payload
        elif isinstance(raw_payload, dict):
            # Try common 2026 keys: 'data', 'markets', or 'result'
            markets = raw_payload.get('data', raw_payload.get('markets', []))
            # If still empty, it might be the new 'ListMarketsResponse' format
            if not markets and 'next_cursor' in raw_payload:
                markets = raw_payload.get('data', [])
        
        print(f"\n🏛️  QUANT COMMAND CENTER: {time.ctime()}")
        print(f"{'MARKET TARGET':<35} | {'VOL (24H)':<10} | {'REBATE EDGE'}")
        print("-" * 75)
        
        count = 0
        for m in markets:
            if not isinstance(m, dict): continue
            if count >= 12: break
            
            # Extract names and volume safely
            name = m.get('description', m.get('question', 'Niche Event'))[:33]
            vol_24h = float(m.get('volume', m.get('volume24hr', 0)) or 0)
            
            # MATH: Maker Rebate Capture (£167/day Target)
            # 0.25% Rebate Rate * 0.5% Volume Capture Estimate
            daily_profit = (vol_24h * 0.005) * 0.0025 
            
            status = "🔥" if daily_profit > 100 else "  "
            
            if vol_24h > 100: # Show any active market
                print(f"{status}{name:<33} | ${vol_24h:>8,.0f} | £{daily_profit:>8.2f}")
                count += 1
                
        if count == 0:
            print(">> STATUS: Scanning for Liquidity... (Try again in 20s)")

    except Exception as e:
        print(f"DIAGNOSTIC: Handshake error. CTO is reviewing structure... ({e})")

if __name__ == "__main__":
    while True:
        get_market_data()
        time.sleep(20)

if __name__ == "__main__":
    while True:
        quant_recon_v3()
        time.sleep(15) # Refreshing every 15s to catch 2026 volatility
