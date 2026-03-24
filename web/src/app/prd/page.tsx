import { FileText, Target, Users, Zap, BarChart3, ShieldCheck } from "lucide-react";

export default function PRDPage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-indigo-400" />
          <span className="text-sm font-medium text-zinc-300">Product Requirements Document (PRD)</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-4xl mx-auto space-y-16 pb-20 text-zinc-300">
          
          <section className="space-y-4">
            <h1 className="text-5xl font-extrabold text-white tracking-tight italic">
              PRODUCT REQUIREMENTS DOCUMENT
            </h1>
            <div className="flex flex-wrap gap-4 text-xs font-mono text-zinc-500 uppercase tracking-widest bg-zinc-900/50 p-4 rounded-lg border border-zinc-800">
              <span>Project: GenAI Capital</span>
              <span className="text-zinc-700">|</span>
              <span>Version: 1.0</span>
              <span className="text-zinc-700">|</span>
              <span className="text-emerald-500">Status: ✅ Implemented</span>
            </div>
          </section>

          <section className="space-y-6">
            <div className="flex items-center gap-3">
              <Target className="w-6 h-6 text-indigo-500" />
              <h2 className="text-2xl font-bold text-white uppercase tracking-wider">1. Product Objective</h2>
            </div>
            <p className="text-lg leading-relaxed text-zinc-400">
              Develop a generative AI-powered investment research assistant that combines structured stock data with unstructured macroeconomic documents to provide contextualized and accurate answers about the financial market.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
              <div className="p-5 bg-zinc-900/40 rounded-2xl border border-zinc-800/50 hover:border-indigo-500/30 transition-all group">
                <h3 className="text-indigo-400 font-bold mb-2 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-500" /> Vision
                </h3>
                <p className="text-sm leading-relaxed">An intelligent assistant for investors to obtain quick insights into companies and trends by combining multiple data sources in one conversational interface.</p>
              </div>
              <div className="p-5 bg-zinc-900/40 rounded-2xl border border-zinc-800/50 hover:border-indigo-500/30 transition-all group">
                <h3 className="text-rose-400 font-bold mb-2 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-rose-500" /> Problem
                </h3>
                <ul className="text-sm space-y-1 list-disc list-inside opacity-80">
                  <li>Fragmented data between spreadsheets/PDFs</li>
                  <li>Time-consuming cross-referencing</li>
                  <li>High risk of hallucination in standard LLMs</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="space-y-6">
            <div className="flex items-center gap-3">
              <Users className="w-6 h-6 text-indigo-500" />
              <h2 className="text-2xl font-bold text-white uppercase tracking-wider">2. Users & Personas</h2>
            </div>
            <div className="space-y-4">
              {[
                { role: "Investment Analyst", need: "Quick company data and macro context. Clear sources and accurate metrics." },
                { role: "Portfolio Manager", need: "Holistic vision for allocation decisions based on micro/macro trends." },
                { role: "Research Academic", need: "Access to original sources and full traceability for correlations." }
              ].map((p, i) => (
                <div key={i} className="flex gap-4 items-start p-4 bg-zinc-950 rounded-xl border border-zinc-900">
                  <div className="w-10 h-10 rounded-full bg-indigo-500/10 flex items-center justify-center text-indigo-400 font-bold shrink-0">{i+1}</div>
                  <div>
                    <h4 className="font-bold text-zinc-100">{p.role}</h4>
                    <p className="text-sm text-zinc-500">{p.need}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="space-y-8">
            <div className="flex items-center gap-3">
              <Zap className="w-6 h-6 text-indigo-500" />
              <h2 className="text-2xl font-bold text-white uppercase tracking-wider">3. Functional Requirements</h2>
            </div>
            
            <div className="relative overflow-x-auto rounded-xl border border-zinc-800">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-zinc-500 uppercase bg-zinc-900/80">
                  <tr>
                    <th className="px-6 py-4">ID</th>
                    <th className="px-6 py-4">Requirement</th>
                    <th className="px-6 py-4 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800">
                  {[
                    { id: "F-01", req: "Structured Data Query (Price, Target, Cap, Yield)", status: "✅" },
                    { id: "F-02", req: "Unstructured Document Query (OECD PDFs via RAG)", status: "✅" },
                    { id: "F-03", req: "Hybrid Queries (Combined context synthesis)", status: "✅" },
                    { id: "F-04", req: "Intelligent Intent Classification", status: "✅" },
                    { id: "F-05", req: "Automated Entity Extraction (Tickers/Names)", status: "✅" },
                    { id: "F-06", req: "Source Identification & Traceability", status: "✅" },
                    { id: "F-07", req: "Financial Data Formatting (Trillions/Billions)", status: "✅" },
                    { id: "F-10", req: "English-only Language Enforcement", status: "✅" },
                  ].map((r, i) => (
                    <tr key={i} className="bg-zinc-950/50 hover:bg-zinc-900/40 transition-colors">
                      <td className="px-6 py-4 font-mono text-indigo-400">{r.id}</td>
                      <td className="px-6 py-4 text-zinc-300">{r.req}</td>
                      <td className="px-6 py-4 text-center">{r.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="space-y-6">
            <div className="flex items-center gap-3">
              <BarChart3 className="w-6 h-6 text-indigo-500" />
              <h2 className="text-2xl font-bold text-white uppercase tracking-wider">4. Success Metrics (KPIs)</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-6 bg-indigo-500/5 rounded-2xl border border-indigo-500/10 text-center">
                <div className="text-3xl font-bold text-white mb-1">95%</div>
                <div className="text-xs text-zinc-500 uppercase">SQL Accuracy</div>
              </div>
              <div className="p-6 bg-emerald-500/5 rounded-2xl border border-emerald-500/10 text-center">
                <div className="text-3xl font-bold text-white mb-1">&lt; 5s</div>
                <div className="text-xs text-zinc-500 uppercase">Avg Response Time</div>
              </div>
              <div className="p-6 bg-amber-500/5 rounded-2xl border border-amber-500/10 text-center">
                <div className="text-3xl font-bold text-white mb-1">1,821</div>
                <div className="text-xs text-zinc-500 uppercase">Verified Companies</div>
              </div>
            </div>
          </section>

          <div className="pt-20 border-t border-zinc-900 flex justify-between items-center opacity-40 italic text-xs">
            <span>GenAI Corporate Intelligence</span>
            <span>Ref: GENAI-CAPITAL-2026</span>
          </div>
        </div>
      </div>
    </>
  );
}
