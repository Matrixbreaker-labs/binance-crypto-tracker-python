# Binance Crypto Futures Data Pipeline

An automated Python script designed to stream live cryptocurrency futures data from the Binance API, manage network congestion using dynamic retry protocols, and structure the data into local Excel documents.

## Key Features

*   **Dynamic Retry Architecture:** Handles HTTP `202 Accepted` status codes automatically by reading the server's `Retry-After` header.
*   **Failover Endpoint Switching:** Rotates through backup network paths if the primary API cluster faces latency or downtime.
*   **Safe Connection Handling:** Implements precise timeouts to prevent hanging processes during high market volatility.
*   **Automated Desktop Export:** Parses the raw network payload via Pandas and locks the compiled dataset directly onto the user's local Desktop.

## System Dependencies

Ensure you have Python 3.8+ installed along with the required libraries. Install them by running:

```bash
pip install requests pandas openpyxl
```

## How It Works

1.  **Extraction Node:** The pipeline attempts a connection to the public endpoints for the designated ticker symbol (Defaults to `BTCUSDT`).
2.  **Silicon Logic Loop:** If the server is busy, the script pauses execution for the exact duration requested by the server before resubmitting the request.
3.  **Compilation Node:** Once a payload is safely fetched, it is timestamped, converted into a DataFrame object, and exported as an `.xlsx` file.

## Execution

Simply execute the core file through your terminal or command prompt:

```bash
python main.py
```

### Script Execution Log Output Example:
```text
[*] Connecting to Binance Public Futures Endpoint...
[+] Live Stream Success! Pair: BTCUSDT | Price: 94250.00
[+] Market data successfully saved to: C:\Users\MatrixBreaker\Desktop\crypto_market_data.xlsx
```

## Error Handling Parameters

*   **HTTP 202 Handling:** Automatically reads `Retry-After` or defaults to a 3-second system cooldown.
*   **Network Failure Loop:** Retries up to 5 times per endpoint before initiating path rotation.
*   **Halt Protocol:** Shuts down execution cleanly using `sys.exit` if all endpoints are completely unreachable to prevent infinite looping.
