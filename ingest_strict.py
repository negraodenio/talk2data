import os, pandas as pd, json, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_ROLE_KEY'])

def run_strict_import(excel_path="equities.xlsx"):
    print(f"🚀 Iniciando Importação Estrita: {excel_path}")
    df = pd.read_excel(excel_path)
    
    # 1. Obter Colunas REAIS do Banco
    res = supabase.table("equities").select("*").limit(1).execute().data
    db_cols = set(res[0].keys()) if res else set()
    print(f"✅ Colunas no Banco: {len(db_cols)}")

    # 2. Mapeamento
    mapping = {
        'isin': 'ISIN', 'ticker': 'Ticker', 'name': 'Company Description',
        'currency': 'Currency', 'stock_price': 'Price', 'price_date': 'Price Date',
        'target_price': 'Target Price', 'target_price_date': 'Target Price Date',
        'dividend_yield': 'Dividend Yield', 'market_cap': 'Market Capitalization',
        'pe_ratio': 'Price to Earning Forward 12M', 'pe_forward_12m': 'Price to Earning Forward 12M',
        'sector_level1': 'Sector - Level 1', 'issuer_country': 'Issuer Country', 'region': 'Region'
    }

    active_map = {db: ex for db, ex in mapping.items() if db in db_cols and ex in df.columns}
    
    records = []
    for _, row in df.iterrows():
        # VALIDATION: Apenas se tiver Ticker E Nome
        t = row.get(active_map['ticker'])
        n = row.get(active_map['name'])
        if pd.isna(t) or pd.isna(n): continue

        rec = {}
        for db, ex in active_map.items():
            val = row[ex]
            if pd.isna(val) or str(val).strip() == "-": rec[db] = None
            else:
                if db in ['stock_price', 'target_price', 'dividend_yield', 'market_cap', 'pe_ratio', 'pe_forward_12m']:
                    try: rec[db] = float(str(val).replace('$','').replace('%','').replace(',','').strip())
                    except: rec[db] = None
                else: rec[db] = str(val).strip()
        records.append(rec)

    print(f"📦 {len(records)} registros prontos.")

    # 3. Inserção (UPSERT)
    inserted = 0
    batch_size = 100
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        try:
            supabase.table("equities").upsert(batch, on_conflict="ticker").execute()
            inserted += len(batch)
            print(f"  Batch {i//batch_size + 1}: {len(batch)} processados.")
        except Exception as e:
            print(f"  ❌ Falha no Batch {i//batch_size + 1}: {e}")

    final_count = supabase.table("equities").select('ticker', count='exact').limit(0).execute().count
    print(f"🏁 Finalizado! Total no banco: {final_count} registros.")

if __name__ == "__main__":
    run_strict_import()
