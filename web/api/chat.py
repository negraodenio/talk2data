from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from openai import OpenAI
import os, json, pandas as pd, PyPDF2, io
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
def classify_query(q):
    prompt = f"Analyze: '{q}'. Return ONLY 'company_specific', 'macro_only', or 'hybrid'."
    res = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return res.choices[0].message.content.strip().lower()

def extract_entities(q):
    prompt = f"Extract company names/tickers from: '{q}'. Return COMMA-SEPARATED list or 'NONE'. Ignore macro names like OECD."
    res = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    content = res.choices[0].message.content.strip()
    return [] if content == "NONE" else [e.strip() for e in content.split(",")]

# --- ENDPOINTS ---
@app.get("/")
def health(): return {"status": "online", "source": "ULTRA-GOLD-ORCHESTRATOR"}

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    q = data.get("question", "")
    
    ctx = ""
    sources = []
    
    q_type = classify_query(q)
    
    # 1. SQL PATH
    if q_type in ['company_specific', 'hybrid']:
        entities = extract_entities(q)
        for ent in entities:
            # Busca por nome ou ticker
            res = supabase.table("equities").select("*").ilike("name", f"%{ent}%").limit(2).execute()
            if not res.data:
                res = supabase.table("equities").select("*").ilike("ticker", f"%{ent}%").limit(2).execute()
            
            if res.data:
                ctx += f"\n[SQL DATA FOR {ent.upper()}]:\n"
                for row in res.data:
                    for k, v in row.items():
                        ctx += f"   - {k}: {v}\n"
                sources.append("SQL Database")

    # 2. RAG PATH
    if q_type in ['macro_only', 'hybrid']:
        try:
            emb_res = client.embeddings.create(input=q, model="openai/text-embedding-3-small")
            emb = emb_res.data[0].embedding
            rag_res = supabase.rpc("match_documents", {"query_embedding": emb, "match_count": 5}).execute()
            if rag_res.data:
                ctx += "\n[MACROECONOMIC REPORTS (PDF RAG)]:\n" + "\n\n".join([d['content'] for d in rag_res.data])
                sources.append("Macro Vector Store")
        except Exception as e:
            print(f"RAG Error: {e}")

    # 3. DETERMINAR LABEL PROFISSIONAL
    final_sources = list(set(sources))
    if "SQL Database" in final_sources and "Macro Vector Store" in final_sources:
        source_label = "Híbrido (SQL + RAG)"
    elif "SQL Database" in final_sources:
        source_label = "Base de Dados SQL (Dados Fundamentais)"
    elif "Macro Vector Store" in final_sources:
        source_label = "Vector Search (Relatórios Macroeconômicos)"
    else:
        source_label = "Nenhuma Fonte Encontrada"

    # 4. SYNTHESIS
    prompt = f"""Use this context to answer: '{q}'
    
    1. STYLE: Professional Investment Analyst. 
    2. DATA: market_cap is in MILLIONS (e.g., 2,425,500 = 2.4 Trillion). Always say 'Trillion' or 'Billion'.
    3. TARGET PRICE: Search for 'target_price' in SQL context. If found, state it clearly.
    4. NO HALLUCINATION: If a metric is missing, say you don't have it.
    
    Context:
    {ctx}"""
    
    comp = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.1)
    
    return {
        "answer": comp.choices[0].message.content,
        "source": source_label,
        "type": q_type
    }
