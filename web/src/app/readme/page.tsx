import { BookOpen, Terminal, Database, Code2 } from "lucide-react";

export default function ReadmePage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-indigo-400" />
          <span className="text-sm font-medium text-zinc-300">Project README</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-3xl mx-auto space-y-12 pb-20 text-zinc-300">
          
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold text-white tracking-tight">GenAI Capital: RAG Assistant</h1>
            <p className="text-lg text-zinc-400">
              A unified AI Orchestrator interfacing natively with Unstructured Macroeconomic PDFs & Structured Equity Data.
            </p>
            <div className="flex items-center justify-center gap-3 pt-4">
              <span className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-medium">Python 3.12</span>
              <span className="px-3 py-1 bg-black text-white border border-zinc-700/50 rounded-full text-xs font-medium">Next.js 14</span>
              <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-medium">Supabase</span>
              <span className="px-3 py-1 bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded-full text-xs font-medium">FastAPI</span>
            </div>
          </div>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-white flex items-center gap-2 border-b border-zinc-800 pb-2">
              <Database className="w-5 h-5 text-indigo-400" /> Architectural Design Patterns
            </h2>
            <p className="leading-relaxed">
              We utilized a <strong>Hybrid RAG + Text-to-SQL Orchestrator</strong> built on top of a unified Supabase Dual-Database engine. Instead of provisioning separate SQL and Vector databases, we use Supabase to cleanly handle both workloads within the same PostgreSQL cluster (using pgvector).
            </p>
            <ul className="list-disc list-inside space-y-2 pl-4 text-zinc-400">
              <li><strong>No LangChain:</strong> The LLM orchestration, prompts, and math vectors are all written globally in native Python for maximum enterprise control.</li>
              <li><strong>Safe Text-to-SQL:</strong> Rather than generating arbitrary SQL string queries which are susceptible to Injection, the engine uses the LLM to strictly extract <em>Entities</em> and maps them via the native Supabase ORM.</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-white flex items-center gap-2 border-b border-zinc-800 pb-2">
              <Terminal className="w-5 h-5 text-indigo-400" /> Vercel Serverless Build
            </h2>
            <p className="leading-relaxed">
              This application strictly adheres to the Next.js Monorepo pattern. The React workspace encapsulates the Python API. When deployed to Vercel, the platform natively invokes `@vercel/python` to expose the backend logic securely over Edge functions.
            </p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-white flex items-center gap-2 border-b border-zinc-800 pb-2">
              <Code2 className="w-5 h-5 text-indigo-400" /> Local Setup Commands
            </h2>
            <div className="bg-zinc-900 rounded-lg p-4 font-mono text-sm border border-zinc-800">
              <p className="text-emerald-400"># 1. Start the Python Backend</p>
              <p>python -m venv venv</p>
              <p>pip install -r requirements.txt</p>
              <p>uvicorn api.chat:app --reload</p>
              <br />
              <p className="text-emerald-400"># 2. Start the Frontend</p>
              <p>npm install</p>
              <p>npm run dev</p>
            </div>
            <p className="text-sm text-zinc-500 italic mt-2">
              Ensure you have populated the .env variables (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, NEXT_PUBLIC_SUPABASE_URL, OPENROUTER_API_KEY).
            </p>
          </section>

        </div>
      </div>
    </>
  );
}
