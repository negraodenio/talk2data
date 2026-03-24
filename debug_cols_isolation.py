import os, pandas as pd, json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))

def debug_columns():
    df = pd.read_excel("equities.xlsx", nrows=10)
    
    # Lista de colunas para testar
    cols_to_test = [
        'isin', 'ticker', 'name', 'currency', 'stock_price', 'price_date', 
        'target_price', 'target_price_date', 'dividend_yield', 'market_cap', 
        'pe_ratio', 'pe_forward_12m', 'sector_level1', 'issuer_country', 'region'
    ]
    
    mapping = {
        'isin': 'ISIN', 'ticker': 'Ticker', 'name': 'Company Description',
        'currency': 'Currency', 'stock_price': 'Price', 'price_date': 'Price Date',
        'target_price': 'Target Price', 'target_price_date': 'Target Price Date',
        'dividend_yield': 'Dividend Yield', 'market_cap': 'Market Capitalization',
        'pe_ratio': 'Price to Earning Forward 12M', 'pe_forward_12m': 'Price to Earning Forward 12M',
        'sector_level1': 'Sector - Level 1', 'issuer_country': 'Issuer Country', 'region': 'Region'
    }

    print("🔍 Testando colunas uma por uma...")
    for db_col in cols_to_test:
        excel_col = mapping.get(db_col)
        if not excel_col or excel_col not in df.columns: continue
        
        test_rec = {'ticker': 'DEBUG_TEST', db_col: None}
        try:
            supabase.table("equities").upsert(test_rec, on_conflict="ticker").execute()
            print(f"  ✓ {db_col}: OK")
        except Exception as e:
            print(f"  ❌ {db_col}: FALHOU - {e}")

if __name__ == "__main__":
    debug_columns()
