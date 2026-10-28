import os
import sys
import time
import requests
import pandas as pd

def get_binance_data(symbol="BTCUSDT"):
    """
    Fetches live crypto futures data from Binance with automatic retry
    handling for 202 Accepted status and backup endpoint switching.
    """
    endpoints = [
        f"https://binance.com{symbol}",
        f"https://binance.com{symbol}",
        f"https://binance.com{symbol}"
    ]
    
    print("[*] Connecting to Binance Public Futures Endpoint...")
    
    for url in endpoints:
        for attempt in range(1, 6):
            try:
                # Set a strict 10-second timeout to handle hanging requests
                response = requests.get(url, timeout=10)
                
                # 200 OK: Data successfully fetched
                if response.status_code == 200:
                    return response.json()
                
                # 202 Accepted: Server is busy processing, must wait and retry
                elif response.status_code == 202:
                    wait_time = int(response.headers.get("Retry-After", 3))
                    print(f"[*] Binance busy (202 Accepted). Retrying... ({attempt}/5) in {wait_time}s")
                    time.sleep(wait_time)
                
                # Other temporary server issues (e.g., 502, 503, 429)
                else:
                    print(f"[-] HTTP Error {response.status_code}. Retrying in 2s...")
                    time.sleep(2)
                    
            except requests.exceptions.RequestException as e:
                print(f"[-] Connection failed: {e}. Retrying execution...")
                time.sleep(2)
                
        print("[-] Switching to backup endpoint...")
        
    print("[-] Pipeline execution halted. All endpoints failed.")
    return None

def export_to_excel(data):
    """Logs data locally and exports it to an Excel sheet on the Desktop."""
    if not data:
        print("[-] No data available to save.")
        return
        
    try:
        # Locate the user's Desktop directory dynamically
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "crypto_market_data.xlsx")
        
        # Prepare DataFrame format
        df = pd.DataFrame([data])
        df['timestamp'] = pd.to_datetime(time.time(), unit='s')
        
        # Exporting dataset
        df.to_excel(file_path, index=False)
        print(f"[+] Market data successfully saved to: {file_path}")
        
    except Exception as e:
        print(f"[-] Failed to export data to Excel: {e}")

if __name__ == "__main__":
    # Execute extraction
    ticker_data = get_binance_data("BTCUSDT")
    
    if ticker_data:
        print(f"[+] Live Stream Success! Pair: {ticker_data.get('symbol')} | Price: {ticker_data.get('price')}")
        export_to_excel(ticker_data)
    else:
        sys.exit("[-] Script terminated: Unable to resolve Binance API streaming pipeline.")
