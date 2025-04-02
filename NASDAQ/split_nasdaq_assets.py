import pandas as pd

print("📄 Loading NASDAQ-listed data...")

try:
    df = pd.read_csv(
        "nasdaq_listed_assets.csv",
        sep='|',
        engine='python',
        quoting=3,  # Ignore quotes
        on_bad_lines='skip',
        skip_blank_lines=True
    )
except Exception as e:
    print("❌ Failed to load file:", e)
    exit()

print("✅ File loaded successfully.")

# Clean column names
df.columns = df.columns.str.strip()

# Clean triple/double quotes and whitespace from all string fields
df = df.applymap(lambda x: x.replace('"', '').strip() if isinstance(x, str) else x)

# Rename 'Symbol' to 'ticker' for consistency
if 'Symbol' in df.columns:
    df = df.rename(columns={"Symbol": "ticker"})

# Check required columns
if 'ETF' not in df.columns or 'Security Name' not in df.columns:
    print("❌ Required columns missing. Found columns:")
    print(df.columns.tolist())
    exit()

# Lowercase version of Security Name for keyword filtering
df['security_name_lower'] = df['Security Name'].astype(str).str.lower()

# 🔎 Filter asset types

print("🔍 Filtering ETFs...")
etfs = df[df['ETF'].str.upper() == 'Y']

print("🔍 Filtering warrants...")
warrants = df[df['security_name_lower'].str.contains('warrant')]

print("🔍 Filtering preferred shares...")
preferreds = df[df['security_name_lower'].str.contains('preferred|preference')]

print("🔍 Filtering bonds...")
bonds = df[df['security_name_lower'].str.contains('bond|note|debenture')]

# Exclude all the above to get regular stocks
print("🔍 Filtering regular stocks...")
excluded = pd.concat([etfs, warrants, preferreds, bonds])
regular_stocks = df[~df.index.isin(excluded.index)]

# 🧹 Keep only the ticker column and drop NaNs
def clean_and_save(name, dataframe):
    tickers = dataframe[['ticker']].dropna()
    tickers.to_csv(f"{name}.csv", index=False)
    print(f"✅ Saved: {name}.csv ({len(tickers)} tickers)")

# 💾 Save all
print("💾 Saving files...")
clean_and_save("regular_stocks", regular_stocks)
clean_and_save("etfs", etfs)
clean_and_save("warrants", warrants)
clean_and_save("preferred_shares", preferreds)
clean_and_save("bonds", bonds)

print("🎉 All files generated successfully.")
