import os
import json
from dotenv import load_dotenv
from supabase import create_client
from openai import OpenAI

load_dotenv(r'c:\Users\denio\Documents\Denio\GenAIExercise\.env')

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

question = "What is the Market Cap of Tesla and how does global inflation impact growth according to the OECD?"
entity = "Tesla"
context_text = ""

# Simulate SQL
sql_res = supabase.table("equities").select("*").ilike("name", f"%{entity}%").limit(3).execute()
if sql_res.data:
    context_text += f"\n--- DADOS ESTRUTURADOS (Relacional SQL) ---\n{str(sql_res.data)}\n"
else:
    print("No SQL data found for Tesla")

# Simulate RAG
res = client.embeddings.create(input=question, model="openai/text-embedding-3-small")
query_embedding = res.data[0].embedding
rag_res = supabase.rpc("match_documents", {"query_embedding": query_embedding, "match_count": 3}).execute()
if rag_res.data:
    docs = [doc['content'] for doc in rag_res.data]
    context_text += f"\n--- DOCUMENTOS MACROECONÔMICOS (Vetorial RAG) ---\n" + "\n\n".join(docs)
else:
    print("No RAG data found")

print("\n--- RAW CONTEXT SENT TO LLM ---")
print(context_text)

prompt = f"""
You are a Senior Investment Research Assistant for GenAI Capital.
The user is asking a financial question. Below is the dynamically extracted context from internal structured databases (SQL) and macroeconomic PDFs (Vector Search).

Dynamically Extracted Context:
{context_text}

User Query: {question}

Critical Rules:
1. You MUST answer ONLY using the provided Extracted Context. Do not invent financial math or prices from your own knowledge.
2. If there is not enough information in the context to answer the question, firmly declare: "I do not have enough information available in the internal sources to answer this."
3. YOUR FINAL RESPONSE MUST ALWAYS BE 100% IN ENGLISH, no matter what language the user types. This is a strict systemic requirement.
"""

print("\n--- FINAL PROMPT ---")
# print(prompt) # Just print the context to save space

completion = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)
print("\n--- LLM ANSWER ---")
print(completion.choices[0].message.content)
