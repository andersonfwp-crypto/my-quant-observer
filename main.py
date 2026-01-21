import requests
import time
import json

# CTO ARCHITECTURE: 2026 ROBUST OBSERVER (V11)
# Features 'Type-Checking' to prevent the 'str' object attribute error.

def target_liquidity():
    # Targets for Jan 2026: Bitcoin $100k, 2026 Midterms, SOL price
    target_tokens = [
        "2174246835183578413151831518315183151831518315183",
        "7348912374891237489123748912374891237489123748912",
        "9981237123123123123123123123123123123123123123123"
    ]
    
    try:
        # Diagnostic: Check Identity first
        geo_resp = requests.get("https://polymarket.com/api/geoblock", timeout=5)
        geo = geo_resp.json()
        
        # Guard against the 'str' error by checking the type
        if isinstance(geo, str):
            print(f"⚠️ DIAGNOSTIC: Geo-API returned text instead of data: {geo[:50]}")
            return

        print(f"\n🌍 HUB: {geo.get('country')} | BLOCKED: {geo.get('blocked')}")
        print(f"📡  ORDERBOOK SCAN: {time.ctime()}")
        print(f"{'ASSET ID':<15} | {'BID':<8} | {'ASK':<8} | {'EST. REBATE'}")
        print("-" * 65)

        for token in target_tokens:
            URL = f"https://clob.polymarket.com/book?token_id={token}"
            response = requests.get(URL, timeout=10)
            
            # Professional data parsing
            try:
                book = response.json()
            except:
                print(f"{token[:15]}... | ❌ API ERROR: Received non-JSON response")
                continue

            if isinstance(book, dict):
                bids = book.get('bids', [])
                asks = book.get('asks', [])
                
                if bids and asks:
                    best_bid = float(bids[0].get('price', 0))
                    best_ask = float(asks[0].get('price', 0))
                    
                    # Turnover Math for £5,000 Portfolio
                    daily_rebate_est = (5000 * 10) * 0.0025 
                    
                    print(f"{token[:15]}... | ${best_bid:<6.3f} | ${best_ask:<6.3f} | £{daily_rebate_est:>8.2f}")
                else:
                    print(f"{token[:15]}... | [NO LIVE ORDERS]")
            else:
                print(f"{token[:15]}... | ⚠️ UNEXPECTED DATA FORMAT")

    except Exception as e:
        print(f"SYSTEM PAUSE: {e}")

if __name__ == "__main__":
    while True:
        target_liquidity()
        time.sleep(15)

if __name__ == "__main__":
    while True:
        global_recon()
        time.sleep(30)
