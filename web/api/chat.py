from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from openai import OpenAI
import os
import json
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

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
else:
    supabase = None

# OpenRouter Client
if OPENROUTER_API_KEY:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
else:
    client = None

@app.get("/")
def read_root():
    return {"message": "Stock Investment Assistant API is running!"}

@app.post("/api/chat")
async def chat(request: Request):
    if not supabase or not client:
        return {"error": "Serviços não configurados. Verifique as variáveis de ambiente."}

    data = await request.json()
    question = data.get("question", "")
    
    context_text = ""
    used_sql = False
    used_rag = False
    
    # ===== PASSO 1: CLASSIFICAÇÃO INTELIGENTE =====
    query_type = classify_query_type(question, client)
    
    # ===== PASSO 2: BUSCA SQL (SEMPRE para perguntas sobre empresas) =====
    if query_type in ["company_specific", "hybrid"]:
        entities_found = extract_companies(question, client)
        
        for ent in entities_found:
            response = supabase.table("equities").select("*").ilike("name", f"%{ent}%").limit(3).execute()
            if not response.data:
                response = supabase.table("equities").select("*").ilike("ticker", f"%{ent}%").limit(3).execute()
            
            if response.data:
                sorted_data = sorted(response.data, key=lambda x: x.get('market_cap') or 0, reverse=True)
                sql_rows = ""
                for row in sorted_data:
                    m_cap = row.get('market_cap')
                    price = row.get('stock_price')
                    m_cap_str = f"{m_cap:,.0f}" if m_cap else "N/A"
                    price_str = f"{price:,.2f}" if price else "N/A"
                    sql_rows += f"- Company: {row.get('name')} ({row.get('ticker')}) | Price: ${price_str} | Market Cap: ${m_cap_str} | PE Ratio: {row.get('pe_ratio')} | Div Yield: {row.get('dividend_yield')}\n"
                
                context_text += f"\n--- STOCK MARKET DATABASE: {ent.upper()} ---\n{sql_rows}\n"
                used_sql = True
    
    # ===== PASSO 3: BUSCA RAG (PARA PERGUNTAS MACRO) =====
    if query_type in ["macro_only", "hybrid"]:
        try:
            res = client.embeddings.create(input=question, model="openai/text-embedding-3-small")
            query_embedding = res.data[0].embedding
            
            response = supabase.rpc("match_documents", {"query_embedding": query_embedding, "match_count": 5}).execute()
            if response.data:
                docs = [doc['content'] for doc in response.data]
                context_text += f"\n--- MACROECONOMIC REPORTS (PDF RAG) ---\n" + "\n\n".join(docs)
                used_rag = True
        except Exception as e:
            print("Erro na busca vetorial:", e)
    
    # ===== PASSO 4: DETERMINAR FONTE =====
    if used_sql and used_rag:
        source_used = "Híbrido (Dados de Mercado + Relatórios Macro)"
    elif used_sql:
        source_used = "Base de Dados SQL (Dados Fundamentais)"
    elif used_rag:
        source_used = "Vector Search (Relatórios Macroeconômicos)"
    else:
        source_used = "Nenhuma Fonte Encontrada"
    
    # ===== PASSO 5: GERAR RESPOSTA =====
    prompt = f"""
    You are a Senior Investment Research Assistant for GenAI Capital.
    The user is asking a financial question. Synthesize an answer based on the context provided below.
    
    [CONTEXT DATA]
    {context_text}
    
    [USER QUERY]
    {question}
    
    [CRITICAL RULES]
    1. ANSWER ONLY using the provided Context.
    2. If the context has BOTH stock data AND macro data, COMBINE them in your answer.
    3. If a specific piece of information is missing, say you don't have it.
    4. FINAL RESPONSE ALWAYS IN ENGLISH.
    5. BE SPECIFIC with numbers and data from the context.
    """
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        answer = f"Erro ao gerar a resposta com o LLM: {e}"

    return {
        "answer": answer,
        "source": source_used,
        "raw_context": context_text
    }

def classify_query_type(question: str, client: OpenAI) -> str:
    """Classifica a pergunta em: company_specific, macro_only, hybrid"""
    prompt = f"""
    Classify this financial question into ONE of these categories:
    - "company_specific": Asks about specific companies, stocks, financial metrics (price, PE, dividend, market cap)
    - "macro_only": Asks about economic trends, inflation, GDP, global markets, OECD, projections
    - "hybrid": Asks about BOTH specific companies AND macro context
    
    Question: "{question}"
    
    Return ONLY the category name.
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip().lower()
    except:
        return "hybrid"

def extract_companies(question: str, client: OpenAI) -> list:
    """Extrai empresas mencionadas na pergunta"""
    ext_prompt = f"""
    Analyze the following financial question: '{question}'. 
    Extract a COMMA-SEPARATED list of ONLY company names or stock tickers mentioned. 
    IMPORTANT: 
    - Ignore macro organizations (OECD, FED, IMF, World Bank)
    - Look for both full names (Amazon) and tickers (AMZN)
    - If no companies are mentioned, return 'NONE'
    
    Return ONLY the names/tickers separated by commas.
    """
    try:
        ext_res = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": ext_prompt}],
            temperature=0
        )
        entity_raw = ext_res.choices[0].message.content.strip()
        if entity_raw == "NONE": return []
        return [e.strip() for e in entity_raw.split(",") if len(e.strip()) > 1]
    except:
        return []
