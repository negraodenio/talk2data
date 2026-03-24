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
    
    # 1. Extração Inteligente da Empresa (Text-to-SQL simplificado / Entity Extraction)
    try:
        ext_prompt = f"Analyze the following financial question: '{question}'. Extract ONLY the name of the publicly traded company or stock ticker mentioned. IMPORTANT: Ignore macroeconomic organizations, government agencies, or reports (e.g., OECD, IMF, FED, G20). Return ONLY the exact company name or ticker. If no specific company is mentioned, answer 'NONE'."
        ext_res = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": ext_prompt}],
            temperature=0
        )
        entity = ext_res.choices[0].message.content.strip().replace(".", "").replace("'", "").replace("\"", "")
        
        # Log de depuração básico (visível no terminal do usuário)
        print(f"--- DEBUG: Entidade Extraída: '{entity}' ---")
        
        if entity != "NONE" and len(entity) > 1:
            # Busca relacional no Supabase (SQL) - Buscamos e ordenamos no Python para estabilidade
            response = supabase.table("equities").select("*").ilike("name", f"%{entity}%").limit(5).execute()
            if not response.data:
                # Tentar por ticker fallback
                response = supabase.table("equities").select("*").ilike("ticker", f"%{entity}%").limit(5).execute()
            
            if response.data:
                # Ordenação Sênior via Python (Mais estável que o Postgrest em MVPs)
                sorted_data = sorted(response.data, key=lambda x: x.get('market_cap') or 0, reverse=True)
                
                sql_rows = ""
                for row in sorted_data:
                    m_cap = row.get('market_cap')
                    price = row.get('stock_price')
                    m_cap_str = f"{m_cap:,.1f}" if m_cap else "N/A"
                    price_str = f"{price:,.2f}" if price else "N/A"
                    
                    sql_rows += f"- Company: {row.get('name')} ({row.get('ticker')}) | Price: ${price_str} | Market Cap: ${m_cap_str} | PE Ratio: {row.get('pe_ratio')} | Div Yield: {row.get('dividend_yield')}\n"
                
                context_text += f"\n--- STOCK MARKET DATABASE (RELATIONAL) ---\n{sql_rows}\n"
                used_sql = True
    except Exception as e:
        print("Erro crítico na SQL:", e)

    # 2. Busca RAG nos PDFs (Intent Router: Só rodar se houver contexto macro ou se o SQL falhou)
    macro_keywords = ["macro", "oecd", "inflation", "growth", "tariffs", "global", "economy", "impact", "trends", "report", "resilience"]
    requires_macro = any(word in question.lower() for word in macro_keywords)
    
    if requires_macro or not used_sql:
        try:
            res = client.embeddings.create(input=question, model="openai/text-embedding-3-small")
            query_embedding = res.data[0].embedding
            
            # Aumentado para 5 para dar mais fôlego à resposta híbrida
            response = supabase.rpc("match_documents", {"query_embedding": query_embedding, "match_count": 5}).execute()
            if response.data:
                docs = [doc['content'] for doc in response.data]
                context_text += f"\n--- MACROECONOMIC REPORTS (PDF RAG) ---\n" + "\n\n".join(docs)
                used_rag = True
        except Exception as e:
            print("Erro na busca vetorial:", e)

    if used_sql and used_rag:
        source_used = "Híbrido (SQL Data + PDF Vectors)"
    elif used_sql:
        source_used = "Base Relacional (SQL Equities)"
    elif used_rag:
        source_used = "Vector Search (Macro PDFs)"
    else:
        source_used = "Nenhuma Fonte Encontrada"

    # 3. Gerar Resposta Final com Agente de Síntese
    prompt = f"""
    You are a Senior Investment Research Assistant for GenAI Capital.
    The user is asking a financial question. Synthesize an answer based on the context provided below.
    
    [CONTEXT DATA]
    {context_text}
    
    [USER QUERY]
    {question}
    
    [CRITICAL RULES]
    1. ANSWER ONLY using the provided Context. 
    2. If the data for a specific part of the query is missing, say you don't have it for that part, but answer the rest.
    3. If the entire context is unrelated, say you don't have enough information.
    4. FINAL RESPONSE ALWAYS IN ENGLISH.
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
