import { BookOpen, Terminal, Database, Code2, ListChecks, PlayCircle, ShieldCheck } from "lucide-react";

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
        <div className="max-w-4xl mx-auto space-y-14 pb-20 text-zinc-300">
          
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold text-white tracking-tight">GenAI Capital: RAG Assistant</h1>
            <p className="text-lg text-emerald-400 font-medium">Senior AI Engineer Technical Assessment</p>
            <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
              A unified AI Orchestrator interfacing natively with Unstructured Macroeconomic PDFs & Structured Equity Data.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-3 pt-4">
              <span className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-medium">Python 3.12</span>
              <span className="px-3 py-1 bg-black text-white border border-zinc-700/50 rounded-full text-xs font-medium">Next.js 14</span>
              <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-medium">Supabase</span>
              <span className="px-3 py-1 bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded-full text-xs font-medium">FastAPI</span>
              <span className="px-3 py-1 bg-zinc-800 text-zinc-100 border border-zinc-700/50 rounded-full text-xs font-medium">Vercel</span>
              <span className="px-3 py-1 bg-orange-500/10 text-orange-400 border border-orange-500/20 rounded-full text-xs font-medium">Cloudflare</span>
            </div>
          </div>

          <section className="space-y-4 bg-zinc-900/40 p-6 rounded-2xl border border-zinc-800/50">
            <h2 className="text-2xl font-semibold text-white flex items-center gap-2 border-b border-zinc-800 pb-2">
              <Database className="w-5 h-5 text-indigo-400" /> Architectural Design Patterns
            </h2>
            <p className="leading-relaxed">
              We utilized a <strong>Hybrid RAG + Text-to-SQL Orchestrator</strong> built on top of a unified Supabase Dual-Database engine. Instead of provisioning separate SQL and Vector databases, we use Supabase to cleanly handle both workloads within the same PostgreSQL cluster (using pgvector).
            </p>
            <ul className="space-y-4 mt-4">
              <li className="flex gap-3">
                <span className="text-indigo-400 shrink-0">■</span>
                <div>
                  <strong className="text-zinc-200">No LangChain:</strong>
                  <p className="text-sm text-zinc-400 mt-1">The LLM orchestration, prompts, and math vectors are all written globally in native Python for maximum enterprise control.</p>
                </div>
              </li>
              <li className="flex gap-3">
                <span className="text-indigo-400 shrink-0">■</span>
                <div>
                  <strong className="text-zinc-200">Safe Text-to-SQL:</strong>
                  <p className="text-sm text-zinc-400 mt-1">Rather than generating arbitrary SQL string queries which are susceptible to Injection, the engine uses the LLM to strictly extract <em>Entities</em> and maps them via the native Supabase ORM.</p>
                </div>
              </li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-white flex items-center gap-2 border-b border-zinc-800 pb-2">
              <ListChecks className="w-5 h-5 text-indigo-400" /> Fulfillment of Core Requirements
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left border-collapse">
                <thead className="bg-zinc-900/80 text-zinc-300">
                  <tr>
                    <th className="p-4 border border-zinc-800 rounded-tl-lg font-semibold w-1/3">Requirement</th>
                    <th className="p-4 border border-zinc-800 rounded-tr-lg font-semibold">Implementation Evidence</th>
                  </tr>
                </thead>
                <tbody className="text-zinc-400">
                  <tr className="hover:bg-zinc-900/30 transition-colors">
                    <td className="p-4 border border-zinc-800 text-zinc-200 font-medium">1. Utilize Python</td>
                    <td className="p-4 border border-zinc-800">The entire backend parsing, embedding, and LLM Orchestration logic is built in Native Python (<code>web/api/chat.py</code>).</td>
                  </tr>
                  <tr className="hover:bg-zinc-900/30 transition-colors">
                    <td className="p-4 border border-zinc-800 text-zinc-200 font-medium">2. Relational Database</td>
                    <td className="p-4 border border-zinc-800">Data sourced from <code>equities.xlsx</code> was loaded into a 3NF-compliant Supabase PostgreSQL instance. Safely queried bypassing SQL-Injection risks.</td>
                  </tr>
                  <tr className="hover:bg-zinc-900/30 transition-colors">
                    <td className="p-4 border border-zinc-800 text-zinc-200 font-medium">3. Vector Database</td>
                    <td className="p-4 border border-zinc-800">Macro reports are semantically matched against user queries via Cosine Similarity powered by OpenAI and Supabase <code>pgvector</code>.</td>
                  </tr>
                  <tr className="hover:bg-zinc-900/30 transition-colors">
                    <td className="p-4 border border-zinc-800 text-zinc-200 font-medium">4. NO LangChain / Wrappers</td>
                    <td className="p-4 border border-zinc-800">Zero orchestration libraries were used. Semantic routing, retrieval, and synthesis are executed programmatically via the raw OpenAI SDK.</td>
                  </tr>
                  <tr className="hover:bg-zinc-900/30 transition-colors">
                    <td className="p-4 border border-zinc-800 text-zinc-200 font-medium">5. English Localization</td>
                    <td className="p-4 border border-zinc-800">All UI components, responses, and API System Prompts are strictly enforced in business-level English natively via systemic instruction overrides.</td>
                  </tr>
                  <tr className="hover:bg-zinc-900/30 transition-colors">
                    <td className="p-4 border border-zinc-800 text-zinc-200 font-medium">6. User Interface (Bonus)</td>
                    <td className="p-4 border border-zinc-800">Elevated beyond a CLI script: Contains a Full-Stack modern Next.js 14 Application deployed via Vercel Edge Serverless Functions.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-white flex items-center gap-2 border-b border-zinc-800 pb-2">
              <ShieldCheck className="w-5 h-5 text-indigo-400" /> Production & Security Roadmap
            </h2>
            <p className="leading-relaxed text-sm">
              While this is a 48h MVP, it was uniquely structured on the Next.js+Supabase monolithic stack to allow immediate scale into production:
            </p>
            <ul className="list-disc list-inside space-y-2 pl-4 text-sm text-zinc-400">
              <li><strong>Supabase Auth (JWT):</strong> The architecture is prepared to inject JWT Bearer Tokens from the frontend to the Python API, enabling isolated, secure user chat histories.</li>
              <li><strong>Row Level Security (RLS):</strong> By migrating from Anon Keys to Authenticated Keys, Postgres RLS can govern which investor sees which equity data natively at the database layer.</li>
            </ul>
          </section>

          <section className="grid md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold text-white flex items-center gap-2 border-b border-zinc-800 pb-2">
                <Terminal className="w-5 h-5 text-indigo-400" /> Vercel Serverless Build
              </h2>
              <p className="leading-relaxed text-sm">
                This application strictly adheres to the Next.js Monorepo pattern. The React workspace encapsulates the Python API. When deployed to Vercel, the platform natively invokes `@vercel/python` to expose the backend logic securely over Edge functions.
              </p>
            </div>
            
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold text-white flex items-center gap-2 border-b border-zinc-800 pb-2">
                <Code2 className="w-5 h-5 text-indigo-400" /> Local Setup Commands
              </h2>
              <div className="bg-black rounded-lg p-4 font-mono text-xs border border-zinc-800 text-zinc-400">
                <p className="text-emerald-500 mb-1"># Python Backend</p>
                <p>python -m venv venv</p>
                <p>pip install -r web/requirements.txt</p>
                <p>uvicorn web.api.chat:app --reload</p>
                <br />
                <p className="text-emerald-500 mb-1"># Frontend React</p>
                <p>cd web</p>
                <p>npm install</p>
                <p>npm run dev</p>
              </div>
            </div>
          </section>

          <section className="space-y-4 bg-indigo-950/20 p-6 rounded-2xl border border-indigo-500/20">
            <h2 className="text-2xl font-semibold text-white flex items-center gap-2 border-b border-indigo-500/30 pb-2">
              <PlayCircle className="w-5 h-5 text-indigo-400" /> Example Queries to Test
            </h2>
            <ul className="space-y-3 mt-4 text-sm text-zinc-300">
              <li><strong className="text-indigo-400">[Vector Search]</strong> "What does the OECD report mention about global growth resilience?"</li>
              <li><strong className="text-emerald-400">[Relational SQL]</strong> "What is the target price and current status of Microsoft?"</li>
              <li><strong className="text-fuchsia-400">[Hybrid RAG]</strong> "What is the Target Price of Tesla and how does global inflation impact growth according to the OECD?"</li>
              <li><strong className="text-rose-400">[Guardrail Fallback]</strong> "What is the target price of FakeCompany Ltd?" (Will trigger the "Data Not Available" security override).</li>
            </ul>
          </section>

        </div>
      </div>
    </>
  );
}
