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
def extract_entities(q):
    # SENIOR: Return only clean keywords. E.g., 'Amazon (AMZN US)' -> 'Amazon, AMZN'
    prompt = f"Extract only clean company names/tickers from: '{q}'. Return COMMA-SEPARATED list (e.g. 'Amazon, MSFT'). Return 'NONE' if no companies found."
    res = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0)
    content = res.choices[0].message.content.strip()
    if content == "NONE": return []
    return [e.strip().split(" ")[0] for e in content.split(",") if len(e.strip()) > 1]

# --- ENDPOINTS ---
@app.get("/")
def health(): return {"status": "online", "source": "ULTRA-GOLD-ORCHESTRATOR-V6-SENIOR"}

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    q = data.get("question", "")
    
    ctx = ""
    sources = []
    
    # 1. FUZZY SQL SEARCH (SENIOR FIX)
    entities = extract_entities(q)
    for ent in entities:
        # SENIOR: Search both ticker and name by the first word of the entity
        clean_ent = ent.split(" ")[0].strip("()[],")
        res = supabase.table("equities").select("*").or_(f"ticker.ilike.%{clean_ent}%,name.ilike.%{clean_ent}%").limit(2).execute()
        
        if res.data:
            ctx += f"\n--- [SQL DATA: {clean_ent.upper()}] ---\n"
            for row in res.data:
                for k, v in row.items(): ctx += f"   - {k}: {v}\n"
            sources.append("SQL Database")

    # 2. RAG SEARCH (Always-on)
    try:
        emb_res = client.embeddings.create(input=q, model="openai/text-embedding-3-small")
        emb = emb_res.data[0].embedding
        rag_res = supabase.rpc("match_documents", {"query_embedding": emb, "match_count": 5}).execute()
        if rag_res.data:
            ctx += "\n--- [MACROECONOMIC REPORTS (PDF RAG)] ---\n" + "\n\n".join([d['content'] for d in rag_res.data])
            sources.append("Macro Vector Store")
    except: pass

    # 3. LABELING (SENIOR FIX)
    final_sources = list(set(sources))
    if "SQL Database" in final_sources and "Macro Vector Store" in final_sources:
        source_label = "Híbrido (Dados de Mercado + Relatórios Macro)"
    elif "SQL Database" in final_sources:
        source_label = "Base de Dados SQL (Dados Fundamentais)"
    elif "Macro Vector Store" in final_sources:
        source_label = "Vector Search (Relatórios Macroeconômicos)"
    else:
        source_label = "Nenhuma Fonte Encontrada"

    # 4. SYNTHESIS
    prompt = f"""Use this context to answer: '{q}'
    Rules for Senior Analyst:
    1. STYLE: Professional Financial Advisor for GenAI Capital.
    2. DATA: 'market_cap' is in MILLIONS (2,425,500 = 2.4 Trillion). Always say 'Trillion' or 'Billion'.
    3. TARGET PRICE: This is MANDATORY. State it clearly if found in SQL context.
    4. NO HALLUCINATION: If the provided context for a ticker is empty, do NOT use internal knowledge.
    
    Context:
    {ctx}"""
    
    comp = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.1)
    
    return {
        "answer": comp.choices[0].message.content,
        "source": source_label
    }
