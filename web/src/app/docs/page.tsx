import { FileText, Database, Blocks, Cpu, Terminal, BarChart3, ChevronRight, Zap, Target } from "lucide-react";

export default function DocsPage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-indigo-400" />
          <span className="text-sm font-medium text-zinc-300">Complete Documentation</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-5xl mx-auto space-y-20 pb-20 text-zinc-300">
          
          {/* Hero Section */}
          <section className="space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-widest">
              System Manual v1.0
            </div>
            <h1 className="text-6xl font-black text-white tracking-tighter italic">
              COMPLETE DOCUMENTATION
            </h1>
            <p className="text-xl text-zinc-400 max-w-3xl leading-relaxed">
              The Stock Investment Research Assistant is a modular GenAI system designed to bridge the gap between 
              structured financial metrics and unstructured economic analysis.
            </p>
          </section>

          {/* Capabilities Grid */}
          <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { title: "Structured Data", desc: "1,821 companies with real-time-simulated metrics (Price, Target, Cap, Yield, P/E).", icon: <Database /> },
              { title: "Unstructured Context", desc: "RAG-powered analysis of macro reports using advanced similarity search.", icon: <Blocks /> },
              { title: "Hybrid Reasoning", desc: "Orchestrated synthesis of multiple data streams for holistic answers.", icon: <Cpu /> },
              { title: "Smart Routing", desc: "Autonomous intent detection and entity extraction via senior LLM logic.", icon: <Zap /> },
            ].map((c, i) => (
              <div key={i} className="p-8 bg-zinc-900/30 rounded-3xl border border-zinc-800/50 hover:bg-zinc-900/50 transition-all group">
                <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-6 group-hover:scale-110 transition-transform">
                  {c.icon}
                </div>
                <h3 className="text-xl font-bold text-white mb-2">{c.title}</h3>
                <p className="text-sm text-zinc-500 leading-relaxed">{c.desc}</p>
              </div>
            ))}
          </section>

          {/* Architecture Visual */}
          <section className="space-y-8">
            <h2 className="text-3xl font-bold text-white flex items-center gap-3 italic">
              <Target className="w-8 h-8 text-indigo-500" /> System Architecture
            </h2>
            <div className="bg-zinc-950 p-10 rounded-3xl border border-zinc-800 relative overflow-hidden">
               <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/5 blur-[100px] rounded-full" />
               <div className="relative font-mono text-xs space-y-6">
                  <div className="flex items-center gap-4 text-zinc-500">
                    <span className="shrink-0 bg-zinc-900 px-3 py-1 rounded border border-zinc-800">Interface Layer</span>
                    <div className="flex-1 h-px bg-zinc-900" />
                    <span className="text-indigo-400 font-bold">CLI / WEB FRONTEND</span>
                  </div>
                  
                  <div className="ml-10 border-l border-zinc-800 pl-10 space-y-4">
                    <div className="p-4 bg-zinc-900/80 rounded-xl border border-indigo-500/20 shadow-lg">
                      <div className="text-indigo-400 font-bold mb-2">PYTHON ORCHESTRATOR</div>
                      <div className="grid grid-cols-2 gap-4 text-[10px] text-zinc-500">
                        <div>• Intent Classification</div>
                        <div>• Entity Extraction</div>
                        <div>• Data Synthesis</div>
                        <div>• Source Labeling</div>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-zinc-500">
                    <span className="shrink-0 bg-zinc-900 px-3 py-1 rounded border border-zinc-800">Data Layer</span>
                    <div className="flex-1 h-px bg-zinc-900" />
                    <span className="text-emerald-400 font-bold">SUPABASE INFRASTRUCTURE</span>
                  </div>
                  
                  <div className="ml-10 grid grid-cols-2 gap-6">
                    <div className="p-4 bg-zinc-900/50 rounded-xl border border-zinc-800">
                      <div className="text-emerald-400 font-bold mb-1 uppercase tracking-tighter">Relational (SQL)</div>
                      <div className="text-zinc-500">equities table (1,821 stocks)</div>
                    </div>
                    <div className="p-4 bg-zinc-900/50 rounded-xl border border-zinc-800">
                      <div className="text-emerald-400 font-bold mb-1 uppercase tracking-tighter">Vector (RAG)</div>
                      <div className="text-zinc-500">documents table (pgvector)</div>
                    </div>
                  </div>
               </div>
            </div>
          </section>

          {/* Processing Examples */}
          <section className="space-y-10">
            <h2 className="text-3xl font-bold text-white italic">Processing Flow & Q&A</h2>
            <div className="space-y-4">
              {[
                { 
                  q: "What is Microsoft's target price?", 
                  type: "SQL Query", 
                  ans: "Microsoft's target price is $600.00. Source: SQL Database" 
                },
                { 
                  q: "How does inflation affect tech stocks like Amazon?", 
                  type: "Hybrid Query", 
                  ans: "Amazon's target price is $270.00. Macro context: Inflation pressures tech margins due to higher cost of capital... Source: Hybrid" 
                },
                { 
                  q: "What does OECD say about 2026 GDP?", 
                  type: "RAG Query", 
                  ans: "OECD reports suggest primary risks include trade barriers and fiscal instability... Source: Macro Reports" 
                }
              ].map((ex, i) => (
                <div key={i} className="bg-zinc-900/20 border border-zinc-800 p-6 rounded-2xl hover:border-indigo-500/20 transition-all">
                  <div className="flex items-center gap-2 mb-4">
                    <span className="text-[10px] font-bold uppercase tracking-widest bg-zinc-800 px-2 py-0.5 rounded text-zinc-400">{ex.type}</span>
                  </div>
                  <div className="space-y-3">
                    <div className="flex gap-3">
                      <ChevronRight className="w-4 h-4 text-indigo-500 shrink-0 mt-1" />
                      <p className="text-zinc-200 font-medium">{ex.q}</p>
                    </div>
                    <div className="ml-7 p-4 bg-zinc-950/50 rounded-xl border border-zinc-900 text-sm text-zinc-400">
                      {ex.ans}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Footer Metrics */}
          <section className="bg-gradient-to-br from-indigo-500/10 to-transparent p-10 rounded-3xl border border-indigo-500/10">
             <div className="flex flex-wrap gap-12 justify-center">
                <div className="text-center">
                  <div className="text-4xl font-black text-white mb-1">1,821</div>
                  <div className="text-[10px] text-zinc-500 uppercase tracking-widest font-bold">Stocks</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-black text-white mb-1">~5s</div>
                  <div className="text-[10px] text-zinc-500 uppercase tracking-widest font-bold">Latency</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-black text-white mb-1">100%</div>
                  <div className="text-[10px] text-zinc-500 uppercase tracking-widest font-bold">Compliance</div>
                </div>
             </div>
          </section>

          <footer className="pt-10 border-t border-zinc-900 opacity-20 text-[10px] font-mono tracking-widest uppercase flex justify-between">
            <span>GenAI Capital Corporate Intelligence</span>
            <span>2026.03.24</span>
          </footer>
        </div>
      </div>
    </>
  );
}
