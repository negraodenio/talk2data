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
        ext_prompt = f"Analyze the following question: '{question}'. Extract ONLY the company name or financial ticker mentioned. If none is mentioned, answer 'NONE'. Return ONLY the exact name or ticker, without punctuation."
        ext_res = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": ext_prompt}]
        )
        entity = ext_res.choices[0].message.content.strip()
        
        if entity != "NONE" and len(entity) > 1:
            # Busca relacional no Supabase (SQL)
            response = supabase.table("equities").select("*").ilike("name", f"%{entity}%").limit(3).execute()
            if not response.data:
                # Tentar por ticker fallback
                response = supabase.table("equities").select("*").ilike("ticker", f"%{entity}%").limit(3).execute()
            
            if response.data:
                context_text += f"\n--- STRUCTURED DATA (Relational SQL) ---\n{json.dumps(response.data, indent=2)}\n"
                used_sql = True
    except Exception as e:
        print("Erro na extração de entidade:", e)

    # 2. Busca RAG nos PDFs (Intent Router: Só rodar se houver contexto macro ou se o SQL falhou)
    macro_keywords = ["macro", "oecd", "inflation", "growth", "tariffs", "global", "economy", "impact", "trends", "report", "resilience"]
    requires_macro = any(word in question.lower() for word in macro_keywords)
    
    if requires_macro or not used_sql:
        try:
            res = client.embeddings.create(input=question, model="openai/text-embedding-3-small")
            query_embedding = res.data[0].embedding
            
            response = supabase.rpc("match_documents", {"query_embedding": query_embedding, "match_count": 3}).execute()
            if response.data:
                docs = [doc['content'] for doc in response.data]
                context_text += f"\n--- MACROECONOMIC DOCUMENTS (Vector RAG) ---\n" + "\n\n".join(docs)
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
    The user is asking a financial question. Below is the dynamically extracted context from internal structured databases (SQL) and macroeconomic PDFs (Vector Search).
    
    Dynamically Extracted Context:
    {context_text}
    
    User Query: {question}
    
    Critical Rules:
    1. You MUST answer ONLY using the provided Extracted Context. Look for JSON keys like 'market_cap' or 'stock_price' if the user asks for financial metrics.
    2. If the context provided (SQL or RAG) is entirely missing information for the requested entities, firmly declare: "I do not have enough information available in the internal sources to answer this."
    3. YOUR FINAL RESPONSE MUST ALWAYS BE 100% IN ENGLISH, no matter what language the user types. This is a strict systemic requirement.
    """
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini", # Usando OpenRouter ID
            messages=[{"role": "user", "content": prompt}]
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        answer = f"Erro ao gerar a resposta com o LLM: {e}"

    return {
        "answer": answer,
        "source": source_used,
        "raw_context": context_text
    }
