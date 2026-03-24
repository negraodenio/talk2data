from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from openai import OpenAI
import os, json, pandas as pd, io
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
    sources_avail = []
    
    # 1. SQL SEARCH
    entities = extract_entities(q)
    for ent in entities:
        clean_ent = ent.split(" ")[0].strip("()[],")
        res = supabase.table("equities").select("*").or_(f"ticker.ilike.%{clean_ent}%,name.ilike.%{clean_ent}%").limit(1).execute()
        if res.data:
            ctx += f"\n--- [SQL DATA: {clean_ent.upper()}] ---\n"
            for row in res.data:
                for k, v in row.items(): ctx += f"   - {k}: {v}\n"
            sources_avail.append("SQL Database")

    # 2. RAG SEARCH
    try:
        emb_res = client.embeddings.create(input=q, model="openai/text-embedding-3-small")
        emb = emb_res.data[0].embedding
        rag_res = supabase.rpc("match_documents", {"query_embedding": emb, "match_count": 5}).execute()
        if rag_res.data:
            docs = [d['content'] for d in rag_res.data]
            ctx += "\n--- [MACROECONOMIC REPORTS (PDF RAG)] ---\n" + "\n\n".join(docs)
            sources_avail.append("Macro Vector Store")
    except: pass

    # 3. SYNTHESIS (DYNAMIC LABELING)
    prompt = f"""Target Query: '{q}'
    
    Rules for Senior Analyst:
    1. STYLE: Professional Financial Advisor for GenAI Capital.
    2. DATA: 'market_cap' is in MILLIONS (3,649,450 = 3.6 Trillion). Always say 'Trillion' or 'Billion'.
    3. TARGET PRICE: Search for 'target_price' in SQL context. If found, STATE IT.
    4. NO HALLUCINATION: If context for a company is empty, say NO DATA FOUND.
    5. SOURCE LABELING: You MUST choose the most accurate source tag based on which context data you ACTUALLY use for your answer:
       - 'Base de Dados SQL (Dados Fundamentais)' (If you only use SQL data)
       - 'Vector Search (Relatórios Macroeconômicos)' (If you only use Macro data)
       - 'Híbrido (Dados de Mercado + Relatórios Macro)' (If you use both)
       - 'Nenhuma Fonte Encontrada' (If you use none)

    OUTPUT FORMAT: Return a RAW JSON string with two keys: "answer" and "source".
    
    Context:
    {ctx}"""
    
    comp = client.chat.completions.create(
        model="openai/gpt-4o-mini", 
        messages=[{"role": "user", "content": prompt}], 
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    try:
        res_json = json.loads(comp.choices[0].message.content)
        return {
            "answer": res_json.get("answer", "No data found."),
            "source": res_json.get("source", "Nenhuma Fonte Encontrada")
        }
    except:
        return {
            "answer": comp.choices[0].message.content,
            "source": "Híbrido (Erro de Formatação)"
        }
