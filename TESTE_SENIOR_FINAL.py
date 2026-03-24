import os, json, logging
from supabase import create_client, Client
from openai import OpenAI
from dotenv import load_dotenv

# Configuração
load_dotenv()
if not os.environ.get("SUPABASE_URL"):
    print("ERRO: Configure o .env com SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY e OPENROUTER_API_KEY")
    exit()

supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("OPENROUTER_API_KEY"))

def orquestrador_senior(pergunta):
    print(f"\n[1] ANALISANDO INTENÇÃO: '{pergunta}'")
    
    # --- EXTRAÇÃO DE ENTIDADE ---
    prompt_ext = f"Extract only the main company name or ticker from: '{pergunta}'. Return ONLY the name/ticker or 'NONE'."
    res_ext = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt_ext}], temperature=0)
    entidades = res_ext.choices[0].message.content.strip()
    
    ctx = ""
    fontes_encontradas = []
    
    # --- BUSCA SQL (FUZZY) ---
    if entidades != "NONE":
        for ent in entidades.split(","):
            keyword = ent.strip().split(" ")[0].strip("()[],")
            print(f"[2] BUSCANDO NO BANCO SQL (Ticker/Nome): '{keyword}'...")
            # Busca agressiva por Ticker ou Nome
            res_sql = supabase.table("equities").select("*").or_(f"ticker.ilike.%{keyword}%,name.ilike.%{keyword}%").limit(1).execute()
            
            if not res_sql.data:
                # Tenta busca manual por ticker exato
                res_sql = supabase.table("equities").select("*").ilike("ticker", f"%{keyword}%").limit(1).execute()

            if res_sql.data:
                print(f"    ✅ DADOS ENCONTRADOS: {res_sql.data[0]['ticker']} ({res_sql.data[0]['name'][:30]}...)")
                ctx += f"\n--- [SQL DATABASE DATA: {keyword.upper()}] ---\n"
                for k, v in res_sql.data[0].items(): ctx += f"   - {k}: {v}\n"
                fontes_encontradas.append("SQL")
            else:
                print(f"    ❌ NENHUM DADO SQL PARA: {keyword}")

    # --- BUSCA RAG (PDFs) ---
    print(f"[3] BUSCANDO NO RAG (Relatórios OCDE)...")
    try:
        emb = client.embeddings.create(input=pergunta, model="openai/text-embedding-3-small").data[0].embedding
        res_rag = supabase.rpc("match_documents", {"query_embedding": emb, "match_count": 5}).execute()
        if res_rag.data:
            print(f"    ✅ CONTEXTO MACRO ENCONTRADO: {len(res_rag.data)} fragmentos")
            ctx += "\n--- [MACROECONOMIC PDF CONTEXT] ---\n" + "\n\n".join([d['content'] for d in res_rag.data])
            fontes_encontradas.append("RAG")
        else:
            print("    ❌ NENHUM CONTEXTO RAG ENCONTRADO.")
    except Exception as e:
        print(f"    ⚠️ Erro no RAG: {e}")

    # --- SÍNTESE FINAL ---
    print(f"[4] SINTETIZANDO RESPOSTA ANALÍTICA...")
    prompt_sys = f"""Você é um Assistente de Pesquisa de Investimentos Sênior. 
    Use o contexto abaixo para responder: '{pergunta}'
    
    REGRAS DE OURO (ASSESSMENT):
    1. MARKET CAP: Está em MILHÕES (ex: 3,649,450 = 3.6 Trillion). Sempre converta para Trillions ou Billions.
    2. TARGET PRICE: Se estiver no contexto SQL, você DEVE citar explicitamente.
    3. FONTE: Escolha apenas uma: 'Source: Base de Dados SQL', 'Source: Vector Search' ou 'Source: Híbrido'.
    4. Hallucination: Se não houver dados no contexto, diga que não encontrou nas fontes internas.
    
    Contexto:
    {ctx}"""
    
    comp = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt_sys}], temperature=0.1)
    
    print("\n" + "═"*60)
    print(comp.choices[0].message.content)
    print("═"*60 + "\n")

if __name__ == "__main__":
    print("--- GenAI Capital CLI Research Tool ---")
    while True:
        q = input("\nDigite sua pergunta (ou 'sair'): ")
        if q.lower() in ['sair', 'exit', 'quit']: break
        orquestrador_senior(q)
