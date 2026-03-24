from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from openai import OpenAI
import os, json, logging
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clients
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("OPENROUTER_API_KEY"))

# --- HELPERS ---
def extrair_empresas(q):
    prompt = f"Extract ALL company names or tickers from: '{q}'. Return JSON array with 'name' and 'ticker' keys. If none, return []."
    try:
        res = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0, response_format={"type": "json_object"})
        data = json.loads(res.choices[0].message.content)
        for k in data:
            if isinstance(data[k], list): return data[k]
        return []
    except: return []

def buscar_sql(ent):
    res = []
    kw = ent.get('ticker', ent.get('name', '')).split(" ")[0].strip("()[],")
    if not kw: return []
    # Try ticker and name sequentially
    r = supabase.table("equities").select("*").ilike("ticker", f"%{kw}%").limit(1).execute()
    if r.data: res.extend(r.data)
    else:
        r = supabase.table("equities").select("*").ilike("name", f"%{kw}%").limit(1).execute()
        if r.data: res.extend(r.data)
    return res

# --- ENDPOINT ---
@app.get("/")
def health(): return {"status": "online", "source": "REFINED-SENIOR-GOLD-V9"}

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    q = data.get("question", "")
    
    ctx = ""
    u_sql, u_rag = False, False
    
    # 1. SQL
    corps = extrair_empresas(q)
    for c in corps:
        hits = buscar_sql(c)
        if hits:
            u_sql = True
            for h in hits:
                mcap = float(h.get('market_cap', 0))
                mcap_str = f"${mcap/1000000:.2f} Trillion" if mcap >= 1000000 else f"${mcap/1000:.1f} Billion" if mcap >= 1000 else f"${mcap:.0f} Million"
                ctx += f"\n--- [SQL DATA: {h['name']}] ---\n - Price: ${h['stock_price']}\n - Target: {h.get('target_price', 'N/A')}\n - Market Cap: {mcap_str}\n - Dividend Yield: {h.get('dividend_yield', 'N/A')}\n"

    # 2. RAG
    if len(q.split()) > 2:
        try:
            emb = client.embeddings.create(input=q, model="openai/text-embedding-3-small").data[0].embedding
            rag = supabase.rpc("match_documents", {"query_embedding": emb, "match_count": 5}).execute()
            if rag.data:
                u_rag = True
                ctx += "\n--- [MACROECONOMIC REPORTS (RAG)] ---\n" + "\n\n".join([d['content'] for d in rag.data[:3]])
        except: pass

    # 3. Label
    label = "Híbrido (Dados de Mercado + Relatórios Macro)" if u_sql and u_rag else "Base de Dados SQL (Dados Fundamentais)" if u_sql else "Vector Search (Relatórios Macroeconômicos)" if u_rag else "Nenhuma Fonte Encontrada"
    
    # 4. Final
    prompt = f"Role: Senior Investment Analyst. Answer: '{q}'. Use context: {ctx}. Rule: If context is empty, say 'No data available in our database'. Ensure Market Cap is in Trillions if millions > 1,000,000. \nSource: {label}"
    res = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.1)
    
    return {"answer": res.choices[0].message.content, "source": label}
