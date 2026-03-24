import { Blocks, Layers, Server, LayoutTemplate } from "lucide-react";

export default function ArchitecturePage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <Blocks className="w-5 h-5 text-indigo-400" />
          <span className="text-sm font-medium text-zinc-300">System Architecture</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-4xl mx-auto space-y-12 pb-20">
          
          <section className="space-y-4">
            <h1 className="text-3xl font-bold tracking-tight text-white mb-6">Decoupled Architecture</h1>
            <p className="text-lg text-zinc-400 leading-relaxed">
              The application is built using a modern, scalable, and decoupled architecture. The frontend is fully isolated from the heavy AI orchestration, communicating gracefully via a REST API.
            </p>
          </section>

          <div className="grid md:grid-cols-2 gap-6 mt-8">
            {/* Frontend */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
                <LayoutTemplate className="w-24 h-24 text-blue-500" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
                <LayoutTemplate className="w-5 h-5 text-blue-400" /> Frontend
              </h3>
              <ul className="space-y-3 mt-6 relative z-10 text-zinc-400 text-sm">
                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span> Next.js 14 (App Router)</li>
                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span> React Server Components</li>
                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span> Tailwind CSS & Lucide Icons</li>
                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span> Vercel Edge Deployment</li>
              </ul>
            </div>

            {/* Backend */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
                <Server className="w-24 h-24 text-emerald-500" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
                <Server className="w-5 h-5 text-emerald-400" /> API Gateway
              </h3>
              <ul className="space-y-3 mt-6 relative z-10 text-zinc-400 text-sm">
                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Python 3 & FastAPI</li>
                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Uvicorn ASGI Server</li>
                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Hybrid RAG Orchestrator</li>
                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Serverless Execution ready</li>
              </ul>
            </div>

            {/* Database & LLMs */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 relative overflow-hidden group md:col-span-2">
              <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
                <Layers className="w-32 h-32 text-purple-500" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
                <Layers className="w-5 h-5 text-purple-400" /> Infrastructure Layer (Dual Database)
              </h3>
              <p className="text-sm text-zinc-400 mb-6">Supabase elegantly fulfills the requirement of having both a Relational PostgreSQL Database and a Vector Database within the same unified engine. The relational side strictly manages **1,821 verified equity records** via the <code>pgvector</code> extension.</p>
              
              <div className="grid md:grid-cols-2 gap-8 mt-6 relative z-10">
                <div>
                  <h4 className="text-sm font-semibold text-zinc-300 mb-3 border-b border-zinc-800 pb-2 flex items-center gap-2"><div className="w-2 h-2 bg-blue-500 rounded-full"></div> Relational PostgreSQL (3NF)</h4>
                  <p className="text-xs text-zinc-500 mb-4">
                    <strong>Architectural Note:</strong> While the current MVP securely ingests the raw CSV directly as a flat table for rapid prototyping, the target Production Schema (below) normalizes the structured data into the 3rd Normal Form (3NF) to eliminate data redundancy (e.g., Sector and Country mappings).
                  </p>
                  
                  {/* Tailwind ERD Diagram */}
                  <div className="space-y-4 font-mono text-xs">
                    {/* Sectors Table */}
                    <div className="bg-zinc-950 border border-zinc-800 rounded p-3">
                      <div className="text-blue-400 font-bold mb-1 border-b border-zinc-800 pb-1">sectors</div>
                      <div className="flex justify-between text-zinc-400"><span><span className="text-amber-500">PK</span> id</span><span>INT</span></div>
                      <div className="flex justify-between text-zinc-400"><span>name</span><span>VARCHAR</span></div>
                    </div>
                    {/* Countries Table */}
                    <div className="bg-zinc-950 border border-zinc-800 rounded p-3">
                      <div className="text-blue-400 font-bold mb-1 border-b border-zinc-800 pb-1">countries</div>
                      <div className="flex justify-between text-zinc-400"><span><span className="text-amber-500">PK</span> id</span><span>INT</span></div>
                      <div className="flex justify-between text-zinc-400"><span>name</span><span>VARCHAR</span></div>
                    </div>
                    {/* Equities Table */}
                    <div className="bg-zinc-950 border border-zinc-800 rounded p-3 relative">
                      <div className="absolute -top-4 left-4 w-px h-4 bg-zinc-700"></div>
                      <div className="text-emerald-400 font-bold mb-1 border-b border-zinc-800 pb-1">equities</div>
                      <div className="flex justify-between text-zinc-400"><span><span className="text-amber-500">PK</span> id</span><span>INT</span></div>
                      <div className="flex justify-between text-zinc-400"><span>ticker</span><span>VARCHAR</span></div>
                      <div className="flex justify-between text-zinc-400"><span><span className="text-rose-400">FK</span> sector_id</span><span>INT</span></div>
                      <div className="flex justify-between text-zinc-400"><span><span className="text-rose-400">FK</span> country_id</span><span>INT</span></div>
                      <div className="flex justify-between text-zinc-400"><span>stock_price</span><span>NUMERIC</span></div>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-zinc-300 mb-3 border-b border-zinc-800 pb-2 flex items-center gap-2"><div className="w-2 h-2 bg-purple-500 rounded-full"></div> Vector Database (pgvector)</h4>
                  <p className="text-xs text-zinc-500 mb-4">Unstructured PDF knowledge is chunked and stored in a mathematical vector space alongside the relational data.</p>
                  <div className="bg-zinc-950 border border-zinc-800 rounded p-3 font-mono text-xs">
                      <div className="text-purple-400 font-bold mb-1 border-b border-zinc-800 pb-1">documents (Vector Store)</div>
                      <div className="flex justify-between text-zinc-400"><span><span className="text-amber-500">PK</span> id</span><span>BIGINT</span></div>
                      <div className="flex justify-between text-zinc-400"><span>content</span><span>TEXT</span></div>
                      <div className="flex justify-between text-zinc-400"><span>embedding</span><span>VECTOR(1536)</span></div>
                  </div>
                  
                  <h4 className="text-sm font-semibold text-zinc-300 mt-8 mb-3 border-b border-zinc-800 pb-2">OpenAI Models</h4>
                  <ul className="space-y-2 text-zinc-400 text-sm">
                    <li><code className="text-emerald-400 text-xs">gpt-4o-mini</code> (Orchestration & Synthesis)</li>
                    <li><code className="text-purple-400 text-xs">text-embedding-3-small</code> (Vectorization)</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </>
  );
}
