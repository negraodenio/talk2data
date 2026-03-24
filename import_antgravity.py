import os
import pandas as pd
import numpy as np
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

# Configuração
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
)

class AntgravityImporter:
    """Importador de dados do Antgravity para o Supabase"""
    
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df = None
        self.records = []
        
        # Mapeamento de colunas do Excel para o banco
        self.column_mapping = {
            # Identificação
            'isin': 'ISIN',
            'ticker': 'Ticker',
            'name': 'Company Description',
            
            # Preços e Valuation
            'currency': 'Currency',
            'stock_price': 'Price',
            'price_date': 'Price Date',
            'target_price': 'Target Price',
            'target_price_date': 'Target Price Date',
            'price_52w_highest': 'Price 52W Highest',
            'price_52w_lowest': 'Price 52W Lowest',
            
            # Métricas Financeiras
            'dividend_yield': 'Dividend Yield',
            'beta': 'Beta',
            'avg_daily_shares_traded': 'Average Daily Shares Traded',
            'market_cap': 'Market Capitalization',
            'free_cash_flow_to_sales': 'Free Cash Flow to Sales',
            
            # EPS e P/E
            'eps_fy0': 'Earning Per Share FY0',
            'eps_fy1': 'Earning Per Share FY1',
            'eps_change_fy1': 'Earning Per Share Change FY1',
            'pe_ratio': 'Price to Earning Forward 12M',  # Usando Forward P/E
            'pe_historical_10y': 'Price to Earning Historical 10Y',
            'pe_forward_12m': 'Price to Earning Forward 12M',
            'pe_fy1': 'Price to Earning FY1',
            'pe_fy2': 'Price to Earning FY2',
            
            # ROE e ROCE
            'roe_forward_12m': 'Return on Equity Forward 12M',
            'roe_fy1': 'Return on Equity FY1',
            'roe_fy2': 'Return on Equity FY2',
            'roce_fy1': 'Return on Capital Employed FY1',
            'roce_fy2': 'Return on Capital Employed FY2',
            
            # Dívida
            'net_debt_to_equity_fy1': 'Net Debt to Equity FY1',
            'net_debt_to_equity_fy2': 'Net Debt to Equity FY2',
            'net_debt_to_ebitda_12m': 'Net Debt to EBITDA Forward 12M',
            'ev_to_ebitda_12m': 'Enterprise Value to EBITDA Forward 12M',
            'ebitda_margin_12m': 'EBITDA Margin Forward 12M',
            'net_profit_margin_12m': 'Net Profit Margin Forward 12M',
            
            # Performance
            'relative_performance_ytd': 'Relative Performance YTD',
            'relative_performance_1y': 'Relative Performance One Year',
            'relative_performance_5y': 'Relative Performance Five Year',
            
            # Recomendações
            'recommendation': 'Recommendation',
            'recommendation_date': 'Recommendation Date',
            'focus_list_status': 'Focus List Status',
            
            # Classificação
            'sector_level1': 'Sector - Level 1',
            'industry_level2': 'Industry Group - Level 2',
            'industry_level3': 'Industry - Level 3',
            'sub_industry_level4': 'Sub-Industry - Level 4',
            'issuer_country': 'Issuer Country',
            'tax_rating': 'Tax Rating',
            'pwm_universe': 'PWM Universe',
            'region': 'Region'
        }
    
    def load_data(self):
        """Carrega dados do Excel"""
        print("="*60)
        print("📊 CARREGANDO DADOS DO ANTGRAVITY")
        print("="*60)
        
        if not os.path.exists(self.excel_path):
            print(f"❌ Arquivo não encontrado: {self.excel_path}")
            return False
        
        # Carregar Excel
        self.df = pd.read_excel(self.excel_path)
        print(f"✅ {len(self.df)} registros carregados")
        print(f"   Colunas disponíveis: {len(self.df.columns)}")
        
        return True
    
    def clean_value(self, value, field_type='float'):
        """Limpa e converte valores"""
        if pd.isna(value) or value == "" or str(value).strip() == "-":
            return None
        
        if field_type == 'float':
            try:
                val_str = str(value).strip()
                # Remover caracteres especiais
                val_str = val_str.replace('$', '').replace('%', '').replace(',', '')
                val_str = val_str.replace('(', '-').replace(')', '')
                return float(val_str)
            except:
                return None
        
        elif field_type == 'int':
            try:
                return int(float(value))
            except:
                return None
        
        elif field_type == 'bool':
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ['yes', 'true', '1', 'y']
            return bool(value)
        
        elif field_type == 'date':
            try:
                if isinstance(value, datetime):
                    return value.strftime('%Y-%m-%d')
                return pd.to_datetime(value).strftime('%Y-%m-%d')
            except:
                return None
        
        else:  # string
            return str(value).strip()
    
    def prepare_records(self):
        """Prepara registros para inserção"""
        print("\n📝 PREPARANDO REGISTROS...")
        
        # Processar cada linha
        errors = 0
        for idx, row in self.df.iterrows():
            try:
                record = {}
                
                # Mapear cada coluna
                for db_col, excel_col in self.column_mapping.items():
                    if excel_col in self.df.columns:
                        value = row[excel_col]
                        
                        # Determinar tipo de campo
                        if db_col in ['price_date', 'target_price_date', 'recommendation_date']:
                            cleaned = self.clean_value(value, 'date')
                        elif db_col in ['pwm_universe']:
                            cleaned = self.clean_value(value, 'bool')
                        elif db_col in ['avg_daily_shares_traded']:
                            cleaned = self.clean_value(value, 'int')
                        elif db_col in ['ticker', 'name', 'currency', 'recommendation', 
                                       'focus_list_status', 'sector_level1', 'industry_level2',
                                       'industry_level3', 'sub_industry_level4', 'issuer_country',
                                       'tax_rating', 'region']:
                            cleaned = self.clean_value(value, 'string')
                        else:
                            cleaned = self.clean_value(value, 'float')
                        
                        record[db_col] = cleaned
                
                # Validação mínima
                if record.get('ticker') or record.get('isin'):
                    self.records.append(record)
                else:
                    errors += 1
            except Exception as e:
                errors += 1
        
        print(f"✅ Registros válidos: {len(self.records)}")
        return len(self.records) > 0
    
    def insert_records(self, clear_existing=False):
        """Insere registros no Supabase"""
        if not self.records: return 0
        
        print("\n📤 INSERINDO REGISTROS...")
        
        if clear_existing:
            try:
                supabase.table("equities").delete().neq("id", 0).execute()
                print("  ✅ Dados antigos removidos")
            except: pass
        
        batch_size = 100
        inserted = 0
        for i in range(0, len(self.records), batch_size):
            batch = self.records[i:i+batch_size]
            try:
                supabase.table("equities").upsert(batch, on_conflict="ticker").execute()
                inserted += len(batch)
                print(f"  Batch {i//batch_size + 1}: {len(batch)} processados (total: {inserted})")
            except Exception as e:
                print(f"  ❌ Erro no batch {i//batch_size + 1}: {e}")
        return inserted

    def run(self, clear_existing=False):
        if not self.load_data(): return False
        if not self.prepare_records(): return False
        inserted = self.insert_records(clear_existing)
        print(f"\n✅ {inserted} registros processados com sucesso!")
        return inserted > 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('excel_file')
    parser.add_argument('--clear', action='store_true')
    args = parser.parse_args()
    
    importer = AntgravityImporter(args.excel_file)
    importer.run(clear_existing=args.clear)
