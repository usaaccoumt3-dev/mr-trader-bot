# -*- coding: utf-8 -*-
import time
import requests

print("==================================================")
print("🚀 MR TRADER - AUTOMATED LIVE ALERTS ENGINE 🚀")
print("==================================================")
print("Target App: ntfy.sh/raokaif_trading")
print("Connecting directly to server internet network...\n")

# Configurations
NTFY_URL = "https://ntfy.sh/raokaif_trading"
WATCHLIST = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT"]

def send_ntfy_alert(title, message, priority="default"):
    """Sends a push notification to the ntfy mobile app."""
    try:
        headers = {
            "Title": title,
            "Priority": priority,
            "Tags": "chart_with_upwards_trend,moneybag"
        }
        response = requests.post(NTFY_URL, data=message.encode('utf-8'), headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✅ Alert sent to mobile for {title}!")
        else:
            print(f"❌ Failed to send alert: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Notification Error: {e}")

def fetch_binance_candles(symbol, limit=30):
    """Fetches clean real-time hourly data from Binance without any manual text errors."""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candles = []
            for item in data:
                candles.append({
                    "open": float(item[1]),
                    "high": float(item[2]),
                    "low": float(item[3]),
                    "close": float(item[4]),
                    "vol": float(item[5])
                })
            return candles
    except Exception as e:
        print(f"⚠️ Live API Error for {symbol}: {e}")
    return None

def analyze_market():
    """Scans halal pairs automatically with locked strategies."""
    print(f"\n🔍 [SERVER SCAN TIME: {time.strftime('%Y-%m-%d %H:%M:%S')}]")

    for symbol in WATCHLIST:
        candles = fetch_binance_candles(symbol)
        if not candles or len(candles) < 20:
            continue

        c_close = candles[-1]['close']
        c_low = candles[-1]['low']

        past_window = candles[-16:-1]
        past_highs = [c['high'] for c in past_window]
        past_lows = [c['low'] for c in past_window]
        past_vols = [c['vol'] for c in past_window]

        high_15 = max(past_highs) if past_highs else c_close
        low_15 = min(past_lows) if past_lows else c_close

        triggered_strat = None
        details = ""

        # 1. 🎯 Golden Sniper Pro
        if (high_15 - low_15) > 0 and c_low <= (high_15 - (0.50 * (high_15 - low_15))) and c_close >= (high_15 - (0.618 * (high_15 - low_15))):
            triggered_strat = "Golden Sniper Pro 🎯"
            details = f"Fibonacci 50%-61.8% Retracement zone hit."

        # 2. ⚡ SMC Liquidity Sweep
        elif c_low < low_15 and c_close > low_15:
            triggered_strat = "SMC Liquidity Sweep ⚡"
            details = f"Price swept past 15-hour low ({low_15:.2f}) and rejected upwards."

        # 3. 🛒 Discount Zone + FVG
        elif c_close < ((high_15 + low_15) / 2) and candles[-1]['close'] > candles[-2]['close']:
            triggered_strat = "Discount Zone + FVG 🛒"
            details = f"Price found support inside the structural Discount Zone."

        # 4. 🧱 Order Block Rejection
        elif past_vols and c_low <= past_highs[past_vols.index(max(past_vols))] and c_close > past_lows[past_vols.index(max(past_vols))]:
            triggered_strat = "Order Block Rejection 🧱"
            details = f"Mitigated high-volume institutional block."

        if triggered_strat:
            title = f"📢 LIVE SIGNAL: {symbol}"
            message = (
                f"Strategy: {triggered_strat}\n"
                f"Price: {c_close:.4f}\n"
                f"Zone: {details}\n"
                f"Time: {time.strftime('%H:%M:%S UTC')}"
            )
            print(f"🔥 FOUND SETUP: {symbol} ({triggered_strat})")
            send_ntfy_alert(title, message, priority="high")
        else:
            print(f"   • {symbol}: Checking setups...")

# Continuous Server Loop
while True:
    try:
        analyze_market()
        print("\n💤 Scanning complete. Waiting for next hourly candle close...")
        time.sleep(3600)
    except KeyboardInterrupt:
        print("\n🛑 Stopped.")
        break
    except Exception as e:
        print(f"⚠️ Loop Exception: {e}")
        time.sleep(60)
