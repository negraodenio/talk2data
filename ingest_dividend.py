import os, json, pandas as pd
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))

df = pd.read_excel("equities.xlsx")

def to_float(val):
    try:
        if pd.isna(val) or val == "" or str(val).strip() == "-" or str(val).strip().lower() == "n.a.": return None
        return float(val)
    except:
        return None

# Mapeamento do usuário + Dividend Yield (que validamos que existe como 'Dividend Yield')
df_filtered = pd.DataFrame({
    'ticker': df['Ticker'],
    'name': df['Company'],
    'sector': df['Sector - Level 1'],
    'country': df['Issuer Country'],
    'stock_price': df['Price'].apply(to_float),
    'target_price': df['Target Price'].apply(to_float),
    'dividend_yield': df['Dividend Yield'].apply(to_float)
})

df_filtered = df_filtered.where(pd.notnull(df_filtered), None)
records = json.loads(df_filtered.to_json(orient='records', date_format='iso'))

for r in records:
    for k in r:
        if r[k] == "": r[k] = None

try:
    print("Enriching database with Dividend Yield...")
    supabase.table("equities").delete().neq("id", 0).execute()
    # Lotes de 200
    for i in range(0, len(records), 200):
        batch = records[i:i+200]
        supabase.table("equities").insert(batch).execute()
    print("SUCCESS! Enriched with Dividend Yield.")
except Exception as e:
    print("Error during dividend enrichment:", e)
