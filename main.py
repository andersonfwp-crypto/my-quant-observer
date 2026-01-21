import requests
import time
import json

# CTO ARCHITECTURE: 2026 ELASTIC SNIPER (V13)
# Robust handling for 'Stringified' responses and nested API wrappers.

def hunt_liquidity():
    try:
        # Step 1: Identity Check
        geo_resp = requests.get("https://polymarket.com/api/geoblock", timeout=5)
        geo = geo_resp.json()
        print(f"\n🌍 HUB: {geo.get('country')} | BLOCKED: {geo.get('blocked')}")
        
        # Step 2: Adaptive Market Discovery
        discovery_url = "https://clob.polymarket.com/sampling-simplified-markets"
        resp = requests.get(discovery_url, timeout=10)
        
        # --- ELASTIC WRAPPER LOGIC ---
        raw_data = resp.json()
        markets = []
        
        if isinstance(raw_data, list):
            markets = raw_data
        elif isinstance(raw_data, dict):
            # Polymarket 2026 often wraps in 'data' or 'markets'
            markets = raw_data.get('data', raw_data.get('markets', []))
        
        # Filter for the top 5 'Whale' markets by liquidity
        active_markets = [m for m in markets if isinstance(m, dict) and m.get('active')]
        top_targets = sorted(active_markets, key=lambda x: float(x.get('liquidity', 0) or 0), reverse=True)[:5]

        print(f"📡  LIVE ORDERBOOK FEED: {time.ctime()}")
        print(f"{'MARKET NAME':<35} | {'BID':<7} | {'ASK':<7} | {'DAILY EDGE'}")
        print("-" * 80)

        for m in top_targets:
            # Safely extract the Yes Token ID
            tokens = m.get('tokens', [])
            if not tokens or not isinstance(tokens, list): continue
            
            yes_token = tokens[0].get('token_id')
            name = m.get('description', 'Unknown')[:33]
            
            # Step 3: Direct Orderbook Ping
            book_url = f"https://clob.polymarket.com/book?token_id={yes_token}"
            book_resp = requests.get(book_url, timeout=10)
            book = book_resp.json()
            
            if isinstance(book, dict):
                bids = book.get('bids', [])
                asks = book.get('asks', [])
                
                if bids and asks:
                    best_bid = float(bids[0].get('price', 0))
                    best_ask = float(asks[0].get('price', 0))
                    
                    # Target: £5,000 capital @ 0.25% Rebate (10x Daily Turnover)
                    daily_est = (5000 * 10) * 0.0025 
                    
                    print(f"🔥{name:<33} | ${best_bid:<6.3f} | ${best_ask:<6.3f} | £{daily_est:>8.2f}")
                else:
                    print(f"  {name:<33} | [EMPTY]   | [EMPTY]   | £0.00")

    except Exception as e:
        print(f"DIAGNOSTIC: Type mismatch or API lag. ({e})")

if __name__ == "__main__":
    while True:
        hunt_liquidity()
        time.sleep(20)
