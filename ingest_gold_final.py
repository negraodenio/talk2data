import pandas as pd
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def ingest_gold():
    supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_ROLE_KEY'])
    file_path = r"c:\Users\denio\Documents\Denio\GenAIExercise\equities.xlsx"
    
    print(f"Loading {file_path}...")
    df = pd.read_excel(file_path)
    
    # Mapping for all 74+ potential columns
    # We will prioritize the core fields requested in the assessment:
    # Symbol -> ticker, Name -> name, Sector -> sector, ISIN -> isin, P/E -> pe_ratio, etc.
    
    records = []
    for _, row in df.iterrows():
        ticker = str(row.get('Symbol', '')).strip()
        if not ticker or ticker == 'nan': continue
        
        rec = {
            'ticker': ticker,
            'name': str(row.get('Name', '')),
            'sector': str(row.get('Sector', '')),
            'stock_price': float(row.get('Price', 0)) if pd.notnull(row.get('Price')) else 0,
            'target_price': float(row.get('Target Price', 0)) if pd.notnull(row.get('Target Price')) else 0,
            'dividend_yield': float(row.get('Dividend Yield', 0)) if pd.notnull(row.get('Dividend Yield')) else 0,
            'market_cap': float(row.get('Market Cap', 0)) if pd.notnull(row.get('Market Cap')) else 0,
            'pe_ratio': float(row.get('P/E', 0)) if pd.notnull(row.get('P/E')) else 0,
            'isin': str(row.get('ISIN', '')).strip() if pd.notnull(row.get('ISIN')) else None,
            'currency': str(row.get('Currency', '')),
            'beta': float(row.get('Beta', 0)) if pd.notnull(row.get('Beta')) else 0,
        }
        records.append(rec)
        
    print(f"Ingesting {len(records)} records...")
    # Batch UPSERT
    batch_size = 100
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        try:
            supabase.table('equities').upsert(batch).execute()
            print(f"Uploaded batch {i//batch_size + 1}")
        except Exception as e:
            print(f"Error in batch {i//batch_size + 1}: {e}")

if __name__ == "__main__":
    ingest_gold()
