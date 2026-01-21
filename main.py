import requests
import time

# CTO ARCHITECTURE: 2026 IDENTITY HUB (V14)
# Bridges CLOB (Price) with Gamma (Names) for a professional dashboard.

NAME_CACHE = {}

def get_market_name(token_id):
    """Bridges the ID to a human-readable name using the Gamma metadata engine."""
    if token_id in NAME_CACHE:
        return NAME_CACHE[token_id]
    
    try:
        # 2026 Gamma Discovery Endpoint
        gamma_url = f"https://gamma-api.polymarket.com/markets?token_id={token_id}"
        resp = requests.get(gamma_url, timeout=5).json()
        
        # Gamma returns a list; we take the first match
        if isinstance(resp, list) and len(resp) > 0:
            name = resp[0].get('question', 'Unknown Event')
            NAME_CACHE[token_id] = name[:33]
            return NAME_CACHE[token_id]
    except:
        pass
    return "Scanning Name..."

def live_fund_recon():
    try:
        # Step 1: Health & Identity
        geo = requests.get("https://polymarket.com/api/geoblock", timeout=5).json()
        print(f"\n🌍 HUB: {geo.get('country')} | BLOCKED: {geo.get('blocked')}")
        
        # Step 2: High-Volume Sampling
        # This endpoint is the 'Gold Standard' for finding liquidity in 2026
        discovery_url = "https://clob.polymarket.com/sampling-simplified-markets"
        resp = requests.get(discovery_url, timeout=10).json()
        
        # Handle both List and Dict wrappers (Elastic Logic)
        markets_list = resp if isinstance(resp, list) else resp.get('data', [])
        
        # Sort by liquidity (The fuel for our £5,000/month goal)
        active_markets = [m for m in markets_list if isinstance(m, dict) and m.get('active')]
        top_targets = sorted(active_markets, key=lambda x: float(x.get('liquidity', 0) or 0), reverse=True)[:5]

        print(f"📡  HEDGE FUND DASHBOARD: {time.ctime()}")
        print(f"{'MARKET TARGET':<35} | {'BID':<7} | {'ASK':<7} | {'DAILY EDGE'}")
        print("-" * 80)

        for m in top_targets:
            tokens = m.get('tokens', [])
            if not tokens: continue
            
            yes_token = tokens[0].get('token_id')
            # Use our new Identity Bridge
            display_name = get_market_name(yes_token)
            
            # Step 3: Direct Book Ping for Real-Time Spreads
            book_url = f"https://clob.polymarket.com/book?token_id={yes_token}"
            book = requests.get(book_url, timeout=10).json()
            
            if isinstance(book, dict):
                bids, asks = book.get('bids', []), book.get('asks', [])
                
                if bids and asks:
                    best_bid = float(bids[0].get('price', 0))
                    best_ask = float(asks[0].get('price', 0))
                    
                    # MATH: £5,000 Capital * 10x Daily Turnover * 0.25% Maker Rebate
                    # This is your 'Rent' for providing liquidity.
                    daily_edge = (5000 * 10) * 0.0025 
                    
                    print(f"🔥{display_name:<33} | ${best_bid:<6.3f} | ${best_ask:<6.3f} | £{daily_edge:>8.2f}")
                else:
                    print(f"  {display_name:<33} | [EMPTY]   | [EMPTY]   | £0.00")

    except Exception as e:
        print(f"SYSTEM RECOVERY: {e}")

if __name__ == "__main__":
    while True:
        live_fund_recon()
        time.sleep(20)
