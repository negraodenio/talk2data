import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client
import json

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

print("Reading Excel...")
df = pd.read_excel("equities.xlsx")
print(f"Total rows in Excel: {len(df)}")

def get_col(patterns):
    for p in patterns:
        matches = [c for c in df.columns if p.lower() in str(c).lower()]
        if matches: 
            # Prefer shorter matches (exact is best)
            matches.sort(key=len)
            print(f"Matched '{p}' -> '{matches[0]}'")
            return matches[0]
    return None

col_map = {
    'ticker': get_col(['Ticker']),
    'name': get_col(['Company']) or get_col(['Name']),
    'stock_price': get_col(['Price']),
    'target_price': get_col(['Target Price']),
    'market_cap': get_col(['Market Capitalization', 'Market Cap']),
    'pe_ratio': get_col(['P/E Ratio', 'PE Ratio']),
    'dividend_yield': get_col(['Dividend Yield', 'Yield'])
}

print("FINAL MAPPING:", col_map)

# Verificar se todos foram mapeados
missing = [k for k,v in col_map.items() if v is None]
if missing:
    print(f"FAILED: Missing columns {missing}")
    # Fallback manuals se necessário
    if 'name' in missing: col_map['name'] = 'Company Description'

def to_float(val):
    try:
        if pd.isna(val) or val == "" or str(val).strip() == "-": return 0.0
        return float(val)
    except:
        return 0.0

records = []
errors = 0
for i, row in df.iterrows():
    try:
        rec = {
            'ticker': str(row[col_map['ticker']]),
            'name': str(row[col_map['name']]),
            'stock_price': to_float(row[col_map['stock_price']]),
            'target_price': to_float(row[col_map['target_price']]),
            'market_cap': to_float(row[col_map['market_cap']]),
            'pe_ratio': to_float(row[col_map['pe_ratio']]),
            'dividend_yield': to_float(row[col_map['dividend_yield']])
        }
        records.append(rec)
    except Exception as e:
        if errors < 5: print(f"Row {i} error: {e}")
        errors += 1

print(f"Prepared {len(records)} records. Errors: {errors}")

if len(records) > 0:
    print("Deleting old rows...")
    supabase.table("equities").delete().neq("id", 0).execute()
    print("Inserting new rows...")
    for i in range(0, len(records), 200):
        batch = records[i:i+200]
        supabase.table("equities").insert(batch).execute()
    print("DONE! Check row count now.")
else:
    print("No records to insert. Check mapping.")
