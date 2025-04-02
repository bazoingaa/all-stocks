import pandas as pd

print("📄 Loading NYSE-listed data...")

try:
    df = pd.read_csv(
        "nyse_listed_assets.csv",
        sep='|',
        engine='python',
        quoting=3,
        on_bad_lines='skip',
        skip_blank_lines=True
    )
    print("✅ File loaded successfully.")
    print("🔍 Columns detected:", df.columns.tolist())
except Exception as e:
    print("❌ Failed to load file:", e)
    exit()

# Clean up column names
df.columns = df.columns.str.strip()

# Clean up extra quotes and whitespace in all string values
df = df.applymap(lambda x: x.replace('"', '').strip() if isinstance(x, str) else x)

# Rename 'ACT Symbol' to 'ticker'
if 'ACT Symbol' in df.columns:
    df = df.rename(columns={"ACT Symbol": "ticker"})

# Make sure necessary columns exist
required_cols = ['ticker', 'Security Name', 'ETF']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    print(f"❌ Missing required column(s): {missing}")
    exit()

# Lowercase version of Security Name for pattern matching
df['security_name_lower'] = df['Security Name'].astype(str).str.lower()

# Filter categories
print("🔍 Filtering ETFs...")
etfs = df[df['ETF'].str.upper() == 'Y']

print("🔍 Filtering warrants...")
warrants = df[df['security_name_lower'].str.contains('warrant')]

print("🔍 Filtering preferred shares...")
preferreds = df[df['security_name_lower'].str.contains('preferred|preference')]

print("🔍 Filtering bonds...")
bonds = df[df['security_name_lower'].str.contains('bond|note|debenture')]

print("🔍 Filtering regular stocks...")
excluded = pd.concat([etfs, warrants, preferreds, bonds])
regular_stocks = df[~df.index.isin(excluded.index)]

# Save helper
def clean_and_save(name, dataframe):
    tickers = dataframe[['ticker']].dropna()
    tickers.to_csv(f"{name}.csv", index=False)
    print(f"✅ Saved: {name}.csv ({len(tickers)} tickers)")

# Save files
print("💾 Saving output files...")
clean_and_save("nyse_etfs", etfs)
clean_and_save("nyse_warrants", warrants)
clean_and_save("nyse_preferred_shares", preferreds)
clean_and_save("nyse_bonds", bonds)
clean_and_save("nyse_regular_stocks", regular_stocks)

print("🎉 Done! All files saved.")
