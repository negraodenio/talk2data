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
    prompt = f"Extract only clean company names/tickers from: '{q}'. Return COMMA-SEPARATED list (e.g. 'Amazon'). Return 'NONE' if no companies found."
    res = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0)
    content = res.choices[0].message.content.strip()
    if content == "NONE": return []
    return [e.strip() for e in content.split(",") if len(e.strip()) > 1]

# --- ENDPOINTS ---
@app.get("/")
def health(): return {"status": "online", "compliant": True}

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    q = data.get("question", "")
    
    ctx = ""
    used_sql = False
    used_rag = False
    
    # 1. ALWAYS SEARCH SQL (Parallel)
    entities = extract_entities(q)
    for ent in entities:
        # Search BOTH ticker and name
        clean_ent = ent.split(" ")[0].strip("()[],")
        res = supabase.table("equities").select("*").or_(f"ticker.ilike.%{clean_ent}%,name.ilike.%{clean_ent}%").limit(1).execute()
        
        if res.data:
            ctx += f"\n--- [SQL DATA: {clean_ent.upper()}] ---\n"
            for row in res.data:
                for k, v in row.items(): 
                    ctx += f"   - {k}: {v}\n"
            used_sql = True

    # 2. ALWAYS SEARCH RAG (Always-on, NO length check)
    try:
        emb_res = client.embeddings.create(input=q, model="openai/text-embedding-3-small")
        emb = emb_res.data[0].embedding
        rag_res = supabase.rpc("match_documents", {"query_embedding": emb, "match_count": 5}).execute()
        if rag_res.data:
            docs = [d['content'] for d in rag_res.data]
            ctx += "\n--- [MACROECONOMIC REPORTS (PDF RAG)] ---\n" + "\n\n".join(docs)
            used_rag = True
    except: pass

    # 3. SOURCE LABELING (STRICT)
    if used_sql and used_rag: label = "Híbrido (Dados de Mercado + Relatórios Macro)"
    elif used_sql: label = "Base de Dados SQL (Dados Fundamentais)"
    elif used_rag: label = "Vector Search (Relatórios Macroeconômicos)"
    else: label = "Nenhuma Fonte Encontrada"

    # 4. SYNTHESIS
    prompt = f"""Use the provided context to analyze the following query: '{q}'
    
    Rules for Senior Analyst:
    1. STYLE: Professional Financial Advisor for GenAI Capital.
    2. DATA: 'market_cap' is in MILLIONS (2,425,500 = 2.4 Trillion). Always say 'Trillion' or 'Billion'.
    3. TARGET PRICE: This is MANDATORY. State it clearly if found in SQL context.
    4. NO HALLUCINATION: If the context for a specific field or company is not found, say so.
    5. ANALYSIS: If context exists but is not an answer to a question (e.g., user pasted a report excerpt), provide a brief summary or insightful comment on it.
    
    Context:
    {ctx}"""
    
    comp = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.1)
    
    return {
        "answer": comp.choices[0].message.content,
        "source": label,
        "type": "hybrid_parallel_v7"
    }
