import { Database, Search, ArrowRight, Zap } from "lucide-react";

export default function RAGPage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <Database className="w-5 h-5 text-emerald-400" />
          <span className="text-sm font-medium text-zinc-300">Vector RAG Engine</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-4xl mx-auto space-y-12 pb-20">
          
          <section className="space-y-4">
            <h1 className="text-3xl font-bold tracking-tight text-white mb-6">Retrieval-Augmented Generation (RAG)</h1>
            <p className="text-lg text-zinc-400 leading-relaxed">
              This application implements a custom RAG engine without relying on high-level frameworks like LangChain. 
              By building it from scratch using Python, OpenAI Embeddings, and Supabase's <code className="text-pink-400 bg-pink-400/10 px-1.5 py-0.5 rounded">pgvector</code>, 
              we maintain full control over the retrieval math, context window injection, and guardrails.
            </p>
          </section>

          <section className="space-y-6">
            <h2 className="text-xl font-semibold text-zinc-200 border-b border-zinc-800 pb-2">1. Data Ingestion & Chunking</h2>
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 text-zinc-300 space-y-4">
              <p>Macroeconomic PDFs (like the <strong>BII Global Outlook</strong> and <strong>OECD Report</strong>) are parsed using Python's <code>pypdf</code>.</p>
              <p>Because LLMs cannot read 50-page PDFs at once, the text is split into sequential <strong>Chunks of 1500 characters</strong> with a 200-character overlap.</p>
              <div className="flex items-center gap-4 py-4 opacity-80">
                <div className="flex-1 h-32 bg-zinc-800 rounded flex items-center justify-center border border-zinc-700">Raw PDF Text</div>
                <ArrowRight className="w-6 h-6 text-zinc-500" />
                <div className="flex-1 flex flex-col gap-2">
                  <div className="h-14 bg-emerald-900/30 border border-emerald-500/20 rounded flex items-center justify-center text-sm">Chunk 1</div>
                  <div className="h-14 bg-emerald-900/30 border border-emerald-500/20 rounded flex items-center justify-center text-sm">Chunk 2</div>
                </div>
              </div>
            </div>
          </section>

          <section className="space-y-6">
            <h2 className="text-xl font-semibold text-zinc-200 border-b border-zinc-800 pb-2">2. Vector Search (Cosine Similarity)</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 space-y-4">
                <div className="w-10 h-10 bg-blue-500/10 rounded-xl flex items-center justify-center mb-4">
                  <Search className="w-5 h-5 text-blue-400" />
                </div>
                <h3 className="font-semibold text-white">The Math</h3>
                <p className="text-sm text-zinc-400 leading-relaxed">
                  Every chunk is mapped into a <strong className="text-zinc-200">1536-dimensional array</strong> using OpenAI&apos;s <code className="text-zinc-300 bg-zinc-800/50 px-1.5 py-0.5 rounded text-xs border border-zinc-700">text-embedding-3-small</code> model. When a user asks a question, the question is also embedded into vector space.
                </p>
              </div>
              <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 space-y-4">
                <div className="w-10 h-10 bg-purple-500/10 rounded-xl flex items-center justify-center mb-4">
                  <Database className="w-5 h-5 text-purple-400" />
                </div>
                <h3 className="font-semibold text-white">pgvector Execution</h3>
                <p className="text-sm text-zinc-400 leading-relaxed">
                  We use a custom Stored Procedure (RPC) <code className="text-zinc-300 bg-zinc-800/50 px-1.5 py-0.5 rounded text-xs border border-zinc-700">match_documents</code> in Supabase. It uses the <code className="text-amber-400 bg-amber-400/10 px-1.5 py-0.5 rounded text-xs">{'<=>'}</code> operator to calculate the Cosine Distance, instantly returning the top 3 most semantically similar paragraphs.
                </p>
              </div>
            </div>
          </section>

        </div>
      </div>
    </>
  );
}
