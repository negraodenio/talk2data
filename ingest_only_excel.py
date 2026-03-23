import os, json, pandas as pd
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))

df = pd.read_excel("equities.xlsx")

def to_float(val):
    try:
        if pd.isna(val) or val == "": return None
        return float(val)
    except:
        return None

df_filtered = pd.DataFrame({
    'ticker': df['Ticker'],
    'name': df['Company'],
    'sector': df['Sector - Level 1'],
    'country': df['Issuer Country'],
    'stock_price': df['Price'].apply(to_float),
    'target_price': df['Target Price'].apply(to_float)
})

df_filtered = df_filtered.where(pd.notnull(df_filtered), None)
records = json.loads(df_filtered.to_json(orient='records', date_format='iso'))

for r in records:
    if r['stock_price'] == "": r['stock_price'] = None
    if r['target_price'] == "": r['target_price'] = None
    if r['sector'] == "": r['sector'] = None
    if r['country'] == "": r['country'] = None

try:
    supabase.table("equities").delete().neq("id", 0).execute()
    res = supabase.table("equities").insert(records).execute()
    print(f"Sucesso Total! {len(res.data)} ações (COM País) inseridas.")
except Exception as e:
    err = str(e)
    if 'PGRST204' in err or 'country' in err:
        print("Cache do Supabase ainda não atualizou a coluna 'country'. Fazendo fallback de segurança para insert sem a coluna Country...")
        # Remover country dos recs
        for r in records:
            r.pop('country', None)
        try:
            res = supabase.table("equities").insert(records).execute()
            print(f"Sucesso Parcial! {len(res.data)} ações inseridas (Sem País - Cache pendente).")
        except Exception as e2:
            print("Erro no Fallback:", e2)
    else:
        print("Erro Fatal:", e)

