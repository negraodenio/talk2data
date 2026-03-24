import { Terminal, Cpu, Database, Blocks, ShieldCheck, CircuitBoard, GitBranch } from "lucide-react";

export default function SpecPage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <Cpu className="w-5 h-5 text-emerald-400" />
          <span className="text-sm font-medium text-zinc-300">Technical Specification</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-5xl mx-auto space-y-16 pb-20 text-zinc-300">
          
          <section className="space-y-4">
            <h1 className="text-5xl font-extrabold text-white tracking-tight">TECHNICAL SPECIFICATION</h1>
            <p className="text-xl text-zinc-400">High-Performance Implementation for AI Capital Research</p>
          </section>

          {/* 1. Architecture Overview */}
          <section className="space-y-8">
            <div className="flex items-center gap-3 border-l-4 border-emerald-500 pl-4">
              <h2 className="text-2xl font-bold text-white uppercase tracking-widest">1. Architecture Overview</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 pb-10">
              {[
                { layer: "Presentation", tech: "CLI (Python) / Web (Next.js)", icon: <Terminal className="w-4 h-4" /> },
                { layer: "Orchestration", tech: "FastAPI / Custom Python Logic", icon: <Cpu className="w-4 h-4" /> },
                { layer: "Data Access", tech: "Supabase / pgvector", icon: <Blocks className="w-4 h-4" /> },
                { layer: "Data Source", tech: "PostgreSQL (1,821 stocks)", icon: <Database className="w-4 h-4" /> },
              ].map((l, i) => (
                <div key={i} className="p-4 bg-zinc-900/50 rounded-xl border border-zinc-800">
                  <div className="flex items-center gap-2 text-zinc-500 text-[10px] uppercase font-bold mb-2 tracking-tighter">
                    {l.icon} {l.layer}
                  </div>
                  <div className="text-sm text-zinc-200 font-medium leading-tight">{l.tech}</div>
                </div>
              ))}
            </div>

            <div className="bg-zinc-950 p-8 rounded-3xl border border-zinc-800 font-mono text-xs overflow-x-auto shadow-2xl">
              <div className="text-emerald-500 mb-4">// System Sequence Flow</div>
              <div className="space-y-1">
                <p className="flex gap-4"><span>[1]</span> <span className="text-zinc-500 italic">User Input</span> <span className="text-zinc-300">"Amazon target price + inflation risks"</span></p>
                <p className="flex gap-4"><span>[2]</span> <span className="text-zinc-500 italic">Classification</span> <span className="text-zinc-300">LLM detects "Hybrid" intent</span></p>
                <p className="flex gap-4"><span>[3]</span> <span className="text-zinc-500 italic">Entity Extract</span> <span className="text-zinc-300">"AMZN" | "Amazon.com, Inc."</span></p>
                <p className="flex gap-4"><span>[4]</span> <span className="text-zinc-500 italic">SQL Search</span> <span className="text-zinc-300">Parallel query to equities table</span></p>
                <p className="flex gap-4"><span>[5]</span> <span className="text-zinc-500 italic">Vector Search</span> <span className="text-zinc-300">Embedding generation + Similarity search</span></p>
                <p className="flex gap-4"><span>[6]</span> <span className="text-zinc-500 italic">Synthesis</span> <span className="text-zinc-300">GPT-4o-mini combines structured + unstructured data</span></p>
                <p className="flex gap-4"><span>[7]</span> <span className="text-zinc-500 italic">Return</span> <span className="text-emerald-400 font-bold">Answer + Source: Hybrid</span></p>
              </div>
            </div>
          </section>

          {/* 2. Technical Components */}
          <section className="space-y-8">
            <div className="flex items-center gap-3 border-l-4 border-emerald-500 pl-4">
              <h2 className="text-2xl font-bold text-white uppercase tracking-widest">2. Core Components</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
              <div className="space-y-4">
                <h3 className="text-zinc-100 font-bold flex items-center gap-2"><Database className="w-5 h-5 text-emerald-500" /> Relational DB</h3>
                <p className="text-sm text-zinc-500">Supabase (PostgreSQL) optimized for financial lookups.</p>
                <pre className="bg-zinc-950 p-4 rounded-xl border border-zinc-800 text-[10px] text-zinc-400 overflow-x-auto">
{`CREATE TABLE equities (
  ticker VARCHAR(10) PRIMARY KEY,
  name TEXT,
  target_price NUMERIC,
  market_cap NUMERIC,
  dividend_yield NUMERIC,
  sector_level1 TEXT
);`}
                </pre>
              </div>
              <div className="space-y-4">
                <h3 className="text-zinc-100 font-bold flex items-center gap-2"><CircuitBoard className="w-5 h-5 text-emerald-500" /> Vector Database</h3>
                <p className="text-sm text-zinc-500">pgvector extension with 1536-dim embeddings.</p>
                <pre className="bg-zinc-950 p-4 rounded-xl border border-zinc-800 text-[10px] text-zinc-400 overflow-x-auto">
{`CREATE OR REPLACE FUNCTION match_documents(...)
RETURNS TABLE(...)
ORDER BY embedding <=> query_embedding
LIMIT match_count;`}
                </pre>
              </div>
            </div>
          </section>

          {/* 3. Models */}
          <section className="space-y-6 bg-zinc-900/40 p-10 rounded-3xl border border-zinc-800">
            <h2 className="text-2xl font-bold text-white uppercase tracking-widest flex items-center gap-3">
              <GitBranch className="w-6 h-6 text-emerald-500" /> Models & LLM Integration
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { name: "GPT-4o mini", use: "Entity & Classification", temp: "0.0" },
                { name: "text-embedding-3-small", use: "Vectorization", temp: "N/A" },
                { name: "GPT-4o mini", use: "Final Synthesis", temp: "0.1" },
              ].map((m, i) => (
                <div key={i} className="p-5 bg-zinc-950 rounded-2xl border border-zinc-800">
                  <div className="text-xs text-zinc-600 font-bold uppercase mb-1 tracking-widest">{m.use}</div>
                  <div className="text-lg font-bold text-white mb-2">{m.name}</div>
                  <div className="text-[10px] p-1 bg-zinc-900 w-fit rounded px-2 text-zinc-500">TEMP: {m.temp}</div>
                </div>
              ))}
            </div>
          </section>
          
          <div className="pt-20 text-center opacity-30 text-[10px] font-mono uppercase tracking-[0.2em]">
            Rigor. Accuracy. Traceability. GenAI Capital v1.0
          </div>

        </div>
      </div>
    </>
  );
}
