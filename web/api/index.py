from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from openai import OpenAI
import os, json, pandas as pd, io, logging
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Logging config
logging.basicConfig(level=logging.INFO, filename='web_api_debug.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("orchestrator")

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
    logger.info(f"Entities extracted: {content}")
    if content == "NONE": return []
    return [e.strip() for e in content.split(",") if len(e.strip()) > 1]

# --- ENDPOINTS ---
@app.get("/")
def health(): return {"status": "online", "source": "ULTRA-STABLE-V8-FINAL"}

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    q = data.get("question", "")
    logger.info(f"Incoming: {q}")
    
    ctx = ""
    used_sql = False
    used_rag = False
    
    # 1. HYPER-FUZZY SQL SEARCH
    entities = extract_entities(q)
    for ent in entities:
        keyword = ent.split(" ")[0].strip("()[],")
        logger.info(f"Searching keyword: {keyword}")
        
        # SEARCH EVERYTHING (OR filter: ticker OR name)
        res = supabase.table("equities").select("*").or_(f"ticker.ilike.%{keyword}%,name.ilike.%{keyword}%").limit(2).execute()
        
        if res.data:
            logger.info(f"SQL SUCCESS: Found {len(res.data)} records for {keyword}")
            ctx += f"\n--- [SQL DATABASE: {keyword.upper()}] ---\n"
            for row in res.data:
                used_sql = True
                for k, v in row.items(): ctx += f"   - {k}: {v}\n"
        else:
            # FALLBACK: Try ticker ONLY more aggressively
            res = supabase.table("equities").select("*").ilike("ticker", f"%{keyword}%").limit(1).execute()
            if res.data:
                logger.info(f"SQL FALLBACK SUCCESS: {keyword}")
                ctx += f"\n--- [SQL DATABASE: {keyword.upper()}] ---\n"
                for row in res.data:
                    used_sql = True
                    for k, v in row.items(): ctx += f"   - {k}: {v}\n"
            else:
                logger.warning(f"SQL FAILURE: No records for {keyword}")

    # 2. ALWAYS SEARCH RAG (Always-on)
    try:
        emb_res = client.embeddings.create(input=q, model="openai/text-embedding-3-small")
        emb = emb_res.data[0].embedding
        rag_res = supabase.rpc("match_documents", {"query_embedding": emb, "match_count": 5}).execute()
        if rag_res.data:
            logger.info(f"RAG SUCCESS: Found {len(rag_res.data)} macro segments")
            docs = [d['content'] for d in rag_res.data]
            ctx += "\n--- [MACROECONOMIC PDF RECORDS] ---\n" + "\n\n".join(docs)
            used_rag = True
    except Exception as e:
        logger.error(f"RAG ERROR: {e}")

    # 3. SYNTHESIS (STRICT TAGGING)
    prompt = f"""Use the provided context to analyze: '{q}'
    Rules:
    1. STYLE: Professional Financial Advisor (GenAI Capital).
    2. DATA: 'market_cap' is in MILLIONS (3,649,450 = 3.6 Trillion). Always say 'Trillion' or 'Billion'.
    3. TARGET PRICE: If found in SQL context, STATE it explicitly.
    4. NO HALLUCINATION: If a company's data is missing in context, say NO DATA FOUND.
    5. SOURCE: You MUST end with EXACTLY ONE of these tags on a new line:
       'Source: Base de Dados SQL (Dados Fundamentais)'
       'Source: Vector Search (Relatórios Macroeconômicos)'
       'Source: Híbrido (Dados de Mercado + Relatórios Macro)'
       'Source: Nenhuma Fonte Encontrada'

    Context:
    {ctx}"""
    
    comp = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.1)
    
    raw_answer = comp.choices[0].message.content
    logger.info(f"Answer synthesized. Source extracted via text parsing.")
    
    # 4. PARSE SOURCE
    final_source = "Nenhuma Fonte Encontrada"
    clean_answer = raw_answer
    
    for s in ["Híbrido (Dados de Mercado + Relatórios Macro)", "Base de Dados SQL (Dados Fundamentais)", "Vector Search (Relatórios Macroeconômicos)", "Nenhuma Fonte Encontrada"]:
        if f"Source: {s}" in raw_answer:
            final_source = s
            clean_answer = raw_answer.replace(f"Source: {s}", "").strip()
            break
            
    return {"answer": clean_answer, "source": final_source}
