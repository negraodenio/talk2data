import os, json, logging, re
from supabase import create_client, Client
from openai import OpenAI
from dotenv import load_dotenv

# Logging Config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("assistant")

# Environment
load_dotenv()
REQUIRED = ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "OPENROUTER_API_KEY"]
for var in REQUIRED:
    if not os.environ.get(var):
        print(f"❌ Missing: {var}")
        exit(1)

# Clients
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("OPENROUTER_API_KEY"))

def extrair_empresas(pergunta):
    """Extrai múltiplas empresas da pergunta (JSON Mode)"""
    prompt = f"Extract ALL company names or tickers from: '{pergunta}'. Return JSON array of objects with 'name' and 'ticker'. Example: [{{'name': 'Microsoft', 'ticker': 'MSFT'}}]. If none, return []."
    try:
        res = client.chat.completions.create(
            model="openai/gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}], 
            temperature=0,
            response_format={"type": "json_object"}
        )
        data = json.loads(res.choices[0].message.content)
        # Search for a list inside any key
        for k in data:
            if isinstance(data[k], list): return data[k]
        return []
    except: return []

def buscar_dados_sql(empresa):
    """Busca dados SQL de forma robusta"""
    res = []
    # 1. Ticker
    if empresa.get('ticker'):
        t_res = supabase.table("equities").select("*").ilike("ticker", f"%{empresa['ticker']}%").limit(2).execute()
        if t_res.data: res.extend(t_res.data)
    # 2. Name
    if empresa.get('name') and not res:
        n_res = supabase.table("equities").select("*").ilike("name", f"%{empresa['name']}%").limit(2).execute()
        if n_res.data: res.extend(n_res.data)
    return res

def formatar_dados_sql(dados):
    """Prepara o contexto financeiro"""
    fmt = []
    for d in dados:
        mcap = float(d.get('market_cap', 0))
        if mcap >= 1000000: mcap_str = f"${mcap/1000000:.2f} Trillion"
        elif mcap >= 1000: mcap_str = f"${mcap/1000:.2f} Billion"
        else: mcap_str = f"${mcap:.0f} Million"
        
        fmt.append({
            'name': d.get('name', 'N/A'),
            'ticker': d.get('ticker', 'N/A'),
            'price': d.get('stock_price', 'N/A'),
            'target': d.get('target_price', 'N/A'),
            'cap': mcap_str,
            'pe': d.get('pe_ratio', 'N/A'),
            'yield': f"{float(d.get('dividend_yield', 0)) * 100:.2f}%" if d.get('dividend_yield') else 'N/A',
            'isin': d.get('isin', 'N/A')
        })
    return fmt

def orquestrador_senior(pergunta):
    print(f"\n🚀 ANALISANDO: {pergunta}")
    
    # 1. Classificar e Extrair
    corps = extrair_empresas(pergunta)
    ctx = ""
    used_sql = False
    used_rag = False
    
    # 2. SQL
    if corps:
        print(f"📊 BUSCANDO SQL PARA: {[c.get('ticker', c.get('name')) for c in corps]}")
        for c in corps:
            hits = buscar_dados_sql(c)
            if hits:
                used_sql = True
                fmt_hits = formatar_dados_sql(hits)
                for h in fmt_hits:
                    ctx += f"\n--- [SQL DATABASE: {h['name']}] ---\n - Price: ${h['price']}\n - Target: {h['target']}\n - Market Cap: {h['cap']}\n - ISIN: {h['isin']}\n"
    
    # 3. RAG
    print(f"📄 BUSCANDO RAG NOS RELATÓRIOS OCDE...")
    try:
        emb = client.embeddings.create(input=pergunta, model="openai/text-embedding-3-small").data[0].embedding
        rag = supabase.rpc("match_documents", {"query_embedding": emb, "match_count": 5}).execute()
        if rag.data:
            used_rag = True
            ctx += "\n--- [MACROECONOMIC REPORTS (RAG)] ---\n" + "\n".join([d['content'] for d in rag.data[:3]])
    except Exception as e: print(f"⚠️ RAG Sync Error: {e}")

    # 4. Síntese Final
    source_label = "Source: " + ("Híbrido (Dados de Mercado + Relatórios Macro)" if used_sql and used_rag else "Base de Dados SQL (Dados Fundamentais)" if used_sql else "Vector Search (Relatórios Macroeconômicos)" if used_rag else "Nenhuma Fonte Encontrada")
    
    prompt = f"""Use the context below to answer: '{pergunta}'
    1. STYLE: Senior Financial Analyst. 
    2. TARGET PRICE: Must be explicitly stated if present in SQL.
    3. MARKET CAP: Provided in Millions. Always convert to Trillion/Billion.
    4. Guardrails: No data found? State it. Keep it professional.
    
    Context:
    {ctx}
    
    {source_label}"""
    
    res = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.1)
    
    print("\n" + "="*50)
    print(res.choices[0].message.content)
    print("="*50 + "\n")

if __name__ == "__main__":
    test_conn = supabase.table("equities").select("count", count="exact").execute()
    print(f"✅ Supabase Online. Records: {test_conn.count}")
    while True:
        q = input("\n💡 Digite sua pergunta (ou 'sair'): ")
        if q.lower() in ['sair', 'exit', 'quit']: break
        orquestrador_senior(q)
