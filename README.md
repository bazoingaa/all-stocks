# All-Stocks: The Open List of Every Ticker in Existence

**All-Stocks** is a free, open-source, dataset of every known stock ticker on every major global exchange.

---

## What This Project Includes

- **Full lists of tickers** from:
  - NASDAQ
  - NYSE
  - (Coming soon: ASX, TSX, LSE, BSE, NSE, Euronext, and more)

- **Categorised outputs**:
  - Regular stocks
  - ETFs
  - Bonds
  - Warrants
  - Preferred shares

---

## Usage

- Clone the repo
- Load any of the CSV files (`*.csv`) into your app, script, or database
- All tickers are formatted to be yfinance-compatible where possible

```bash
git clone https://github.com/bazoingaa/all-stocks.git
```

Example using pandas:
```python
import pandas as pd
nasdaq = pd.read_csv("nasdaq_regular_stocks.csv")
print(nasdaq.head())
```
---

## Credits

Created by [@bazoingaa](https://github.com/bazoingaa).

---

## 📂 File Structure
```
all-stocks/
├── nasdaq_regular_stocks.csv
├── nasdaq_etfs.csv
├── nyse_regular_stocks.csv
├── nyse_etfs.csv
├── warrants.csv
├── preferred_shares.csv
├── bonds.csv
└── ... more coming soon
```

