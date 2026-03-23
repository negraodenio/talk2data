import os
import pandas as pd
from supabase import create_client, Client
from openai import OpenAI
from pypdf import PdfReader
from dotenv import load_dotenv

# Carregar do .env
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if not all([SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENROUTER_API_KEY]):
    print("ERRO: Configure SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY e OPENROUTER_API_KEY no arquivo .env")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

def ingest_excel():
    print("--- Ingerindo Excel para SQL ---")
    file_path = "equities.xlsx"
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado na raiz.")
        return

    try:
        df = pd.read_excel(file_path)
        # Vamos padronizar os nomes das colunas
        # Ex: 'Ticker', 'Company Name', 'Sector' -> 'ticker', 'company_name', 'sector'
        df.columns = [c.lower().replace(' ', '_') for c in df.columns]
        
        # Filtrar NaN
        df = df.fillna("")
        
        import json
        data = json.loads(df.to_json(orient='records', date_format='iso'))
        # Limpar tabela antes? Opcional!
        # supabase.table("equities").delete().neq("id", 0).execute()
        
        res = supabase.table("equities").insert(data).execute()
        print(f"Sucesso! {len(res.data)} ações inseridas.")
    except Exception as e:
        print(f"Erro no Excel: {e}")

def ingest_pdfs():
    print("--- Ingerindo PDFs para Vetores ---")
    pdf_folder = "PDF"
    if not os.path.exists(pdf_folder):
        print(f"Pasta {pdf_folder} não encontrada.")
        return

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            try:
                print(f"Processando {filename}...")
                reader = PdfReader(os.path.join(pdf_folder, filename))
                text = "".join(page.extract_text() or "" for page in reader.pages)
                
                if not text.strip():
                    continue

                # Chunking
                chunk_size = 1500
                chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                
                print(f" -> {len(chunks)} chunks gerados.")
                for i, chunk in enumerate(chunks):
                    # Embeddings (verifique se OpenRouter aceita esta chamada sem dar erro)
                    res = client.embeddings.create(input=chunk, model="openai/text-embedding-3-small")
                    embedding = res.data[0].embedding
                    
                    supabase.table("documents").insert({
                        "content": chunk,
                        "metadata": {"source": filename, "chunk": i+1},
                        "embedding": embedding
                    }).execute()
                    
                print(f"+++ {filename} OK!")
            except Exception as e:
                print(f"Erro no arquivo {filename}: {e}")

if __name__ == "__main__":
    print("Iniciando ingestão...")
    ingest_excel()
    ingest_pdfs()
    print("Finalizado!")
