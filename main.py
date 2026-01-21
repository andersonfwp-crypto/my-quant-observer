import requests
import time

# CTO ARCHITECTURE: 2026 AUTO-DISCOVERY SNIPER (V12)
# Automatically finds the top 5 high-volume markets and pulls their Order Books.

def auto_discovery_scan():
    try:
        # Step 1: Identity & Geo Check
        geo = requests.get("https://polymarket.com/api/geoblock", timeout=5).json()
        print(f"\n🌍 HUB: {geo.get('country')} | BLOCKED: {geo.get('blocked')}")
        
        # Step 2: Discover Top 5 Active Tokens
        # We hit the 'sampling' endpoint to find where the whales are trading
        discovery_url = "https://clob.polymarket.com/sampling-simplified-markets"
        discovery_resp = requests.get(discovery_url, timeout=10)
        all_markets = discovery_resp.json()
        
        # Sort by liquidity to find the 'hottest' order books
        active_markets = [m for m in all_markets if m.get('active')]
        top_markets = sorted(active_markets, key=lambda x: float(x.get('liquidity', 0)), reverse=True)[:5]

        print(f"📡  LIVE MARKET DISCOVERY: {time.ctime()}")
        print(f"{'MARKET NAME':<35} | {'BID':<7} | {'ASK':<7} | {'PROFIT/D'}")
        print("-" * 75)

        for m in top_markets:
            # Polymarket tokens have a 'Yes' and 'No' side. We track the 'Yes' side (Token ID)
            # Some APIs use 'tokens', others use 'token_id'
            tokens = m.get('tokens', [])
            if not tokens: continue
            
            yes_token = tokens[0].get('token_id')
            name = m.get('description', 'Unknown')[:33]
            
            # Step 3: Fetch the actual Order Book for this specific token
            book_url = f"https://clob.polymarket.com/book?token_id={yes_token}"
            book = requests.get(book_url, timeout=10).json()
            
            bids = book.get('bids', [])
            asks = book.get('asks', [])
            
            if bids and asks:
                best_bid = float(bids[0].get('price'))
                best_ask = float(asks[0].get('price'))
                
                # Math: £5,000 capital @ 0.25% Maker Rebate (assuming 10 turnovers/day)
                # This is your path to the £5,000/month target.
                daily_est = (5000 * 10) * 0.0025 
                
                print(f"🔥{name:<33} | ${best_bid:<6.3f} | ${best_ask:<6.3f} | £{daily_est:>7.2f}")
            else:
                print(f"  {name:<33} | [EMPTY BOOK]         | £0.00")

    except Exception as e:
        print(f"SYSTEM RECOVERY: {e}")

if __name__ == "__main__":
    while True:
        auto_discovery_scan()
        # Slower sleep to respect the 2026 Rate Limits
        time.sleep(20)
