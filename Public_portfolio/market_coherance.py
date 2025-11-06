"""
Hjermstad Quant • Market Coherence Generator
--------------------------------------------
• Computes daily coherence score across selected indices.
• Writes two JSON files:
    data/coherence.json          -> latest snapshot (for gauge)
    data/coherence_history.json  -> rolling daily history (for chart)
"""

import yfinance as yf
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------
# SETTINGS
# ---------------------------------------------------
DATA_PATH = Path("data")
DATA_PATH.mkdir(exist_ok=True)
SNAPSHOT_FILE = DATA_PATH / "coherence.json"
HISTORY_FILE = DATA_PATH / "coherence_history.json"

# Choose representative indices (or ETFs)
SYMBOLS = ["^GSPC", "^IXIC", "^DJI", "^FTSE", "^N225", "^GDAXI"]

ROLLING_WINDOW = 30   # days for correlation window
HISTORY_LIMIT = 365   # keep one year of daily data

# ---------------------------------------------------
def compute_coherence(df: pd.DataFrame) -> float:
    """Return Hjermstad-style coherence index (0–100)."""
    returns = df.pct_change().dropna()
    corr = returns.corr().abs().values
    n = len(corr)
    coherence = 100 * (np.sum(corr) - n) / (n * (n - 1))
    return round(float(coherence), 2)

# ---------------------------------------------------
def main():
    # 1️⃣ Fetch closing prices
    end = datetime.utcnow()
    start = end - timedelta(days=ROLLING_WINDOW * 2)
    data = yf.download(SYMBOLS, start=start, end=end)["Adj Close"].dropna(how="all")

    # 2️⃣ Compute coherence for latest complete day
    latest_df = data.tail(ROLLING_WINDOW)
    coherence = compute_coherence(latest_df)

    # 3️⃣ Update history
    history = []
    if HISTORY_FILE.exists():
        history = json.loads(HISTORY_FILE.read_text())

    today = end.strftime("%Y-%m-%d")
    # remove any duplicate entry for today
    history = [h for h in history if h["date"] != today]
    history.append({"date": today, "coherence": coherence})

    # trim to limit
    history = history[-HISTORY_LIMIT:]

    # 4️⃣ Write output files
    snapshot = {
        "timestamp": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "coherence": coherence
    }
    SNAPSHOT_FILE.write_text(json.dumps(snapshot, indent=2))
    HISTORY_FILE.write_text(json.dumps(history, indent=2))

    print(f"[{today}] Coherence: {coherence:.2f}")

# ---------------------------------------------------
if __name__ == "__main__":
    main()
