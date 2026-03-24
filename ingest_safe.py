import os, pandas as pd, json, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))

def run_safe_import(excel_path="equities.xlsx"):
    print(f"🚀 Iniciando Importação Segura: {excel_path}")
    df = pd.read_excel(excel_path)
    
    # 1. Obter Colunas REAIS do Banco
    test_rec = supabase.table("equities").select("*").limit(1).execute().data
    db_cols = set(test_rec[0].keys()) if test_rec else set()
    print(f"✅ Colunas detectadas no Supabase: {len(db_cols)}")

    # 2. Mapeamento Desejado (conforme pedido pelo usuário)
    target_mapping = {
        'isin': 'ISIN', 'ticker': 'Ticker', 'name': 'Company Description',
        'currency': 'Currency', 'stock_price': 'Price', 'price_date': 'Price Date',
        'target_price': 'Target Price', 'target_price_date': 'Target Price Date',
        'dividend_yield': 'Dividend Yield', 'market_cap': 'Market Capitalization',
        'pe_ratio': 'Price to Earning Forward 12M', 'pe_forward_12m': 'Price to Earning Forward 12M',
        'sector_level1': 'Sector - Level 1', 'industry_level2': 'Industry Group - Level 2',
        'issuer_country': 'Issuer Country', 'region': 'Region'
        # Adicione outros se necessário, mas esses são os principais.
    }

    # 3. Filtrar Mapeamento (apenas o que existe no DB e no Excel)
    active_mapping = {}
    for db_col, excel_col in target_mapping.items():
        if db_col in db_cols and excel_col in df.columns:
            active_mapping[db_col] = excel_col
    
    print(f"✅ Mapeamento Ativo: {list(active_mapping.keys())}")

    records = []
    for _, row in df.iterrows():
        rec = {}
        for db_col, excel_col in active_mapping.items():
            val = row[excel_col]
            if pd.isna(val) or str(val).strip() == "-": rec[db_col] = None
            else:
                if db_col in ['stock_price', 'target_price', 'dividend_yield', 'market_cap', 'pe_ratio', 'pe_forward_12m']:
                    try:
                        v = str(val).replace('$','').replace('%','').replace(',','').strip()
                        rec[db_col] = float(v)
                    except: rec[db_col] = None
                else: rec[db_col] = str(val).strip()
        
        if rec.get('ticker') or rec.get('isin'): records.append(rec)

    print(f"📦 {len(records)} registros preparados.")

    # 4. Inserção em Batches (UPSERT)
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

    print(f"🏁 Finalizado! {inserted} registros inseridos/atualizados.")

if __name__ == "__main__":
    run_safe_import()
