import { Code, CheckCircle2 } from "lucide-react";

export default function SourceCodePage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <Code className="w-5 h-5 text-cyan-500" />
          <span className="text-sm font-medium text-zinc-300">Source Code (Python)</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-4xl mx-auto space-y-12 pb-20">
          
          <section className="space-y-4">
            <h1 className="text-3xl font-bold tracking-tight text-white mb-6">Backend API (FastAPI)</h1>
            <p className="text-lg text-zinc-400 leading-relaxed border-l-4 border-cyan-500/50 pl-4">
              Below is the core of our application: the <code>api/index.py</code> endpoint. This file receives requests from the Frontend, orchestrates the Text-to-SQL logic alongside the Vector Search (RAG), and handles the final LLM synthesis.
            </p>
          </section>

          <div className="space-y-8">
            
            {/* Block 1 */}
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-500 mt-1" />
                <div>
                  <h3 className="text-zinc-200 font-semibold mb-1">1. Hybrid Routing & Safe Text-to-SQL</h3>
                  <p className="text-sm text-zinc-400">We extract the financial 'Entity' via AI prior to executing any SQL commands to prevent Injection attacks. If the query against the Supabase table yields results, the SQL flow is activated.</p>
                </div>
              </div>
              <div className="bg-black/60 border border-zinc-800 rounded-xl p-4 overflow-x-auto">
                <pre className="text-xs font-mono text-zinc-300 leading-relaxed">
{`# 1. Intelligent Entity Extraction (Safe Text-to-SQL)
try:
    ext_prompt = f"Analyze the following question: '{question}'. Extract ONLY the company name or financial ticker... Return ONLY the exact name, without punctuation."
    ext_res = client.chat.completions.create(...)
    entity = ext_res.choices[0].message.content.strip()
    
    if entity != "NONE" and len(entity) > 1:
        # Relational search in Supabase (SQL)
        response = supabase.table("equities").select("*").ilike("name", f"%{entity}%").limit(3).execute()
        
        if response.data:
            context_text += f"\\n--- STRUCTURED DATA ---\\n{str(response.data)}\\n"
            used_sql = True
except Exception as e:
    print("Entity extraction error:", e)`}
                </pre>
              </div>
            </div>

            {/* Block 2 */}
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-500 mt-1" />
                <div>
                  <h3 className="text-zinc-200 font-semibold mb-1">2. Semantic Vector Search (RAG)</h3>
                  <p className="text-sm text-zinc-400">Simultaneously, we embed the user's question and execute a mathematical Cosine Similarity procedure directly against the Embeddings database (pgvector).</p>
                </div>
              </div>
              <div className="bg-black/60 border border-zinc-800 rounded-xl p-4 overflow-x-auto">
                <pre className="text-xs font-mono text-zinc-300 leading-relaxed">
{`# 2. RAG Search in PDFs (Macro Context)
try:
    res = client.embeddings.create(input=question, model="openai/text-embedding-3-small")
    query_embedding = res.data[0].embedding
    
    # match_count: 3 retrieves the 3 most similar PDF chunks
    response = supabase.rpc("match_documents", {"query_embedding": query_embedding, "match_count": 3}).execute()
    
    if response.data:
        docs = [doc['content'] for doc in response.data]
        context_text += f"\\n--- MACROECONOMIC DOCUMENTS ---\\n" + "\\n\\n".join(docs)
        used_rag = True
except Exception as e:
    print("Vector search error:", e)`}
                </pre>
              </div>
            </div>

            {/* Block 3 */}
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-500 mt-1" />
                <div>
                  <h3 className="text-zinc-200 font-semibold mb-1">3. Synthesis and Dynamic Source Tags</h3>
                  <p className="text-sm text-zinc-400">We pass the combined context to the AI with rigorous Guardrails, explicitly forbidding the invention of values that are not present in the extracted texts above.</p>
                </div>
              </div>
              <div className="bg-black/60 border border-zinc-800 rounded-xl p-4 overflow-x-auto">
                <pre className="text-xs font-mono text-zinc-300 leading-relaxed">
{`# Dynamic calculation for interface context tracking:
if used_sql and used_rag:
    source_used = "Hybrid (SQL Data + PDF Vectors)"
elif used_sql:
    source_used = "Relational Database (SQL Equities)"
elif used_rag:
    source_used = "Vector Search (Macro PDFs)"

# 3. Final Answer Generation with Synthesis Agent
prompt = f"""
You are a Senior Investment Research Assistant for GenAI Capital.
Below is the dynamically extracted context from databases and PDFs.

Dynamically Extracted Context: {context_text}
User Query: {question}

Critical Rules:
1. You MUST answer ONLY using the provided Extracted Context. Do not invent financial math.
2. YOUR FINAL RESPONSE MUST ALWAYS BE 100% IN ENGLISH.
"""
completion = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[...])`}
                </pre>
              </div>
            </div>

          </div>
        </div>
      </div>
    </>
  );
}
