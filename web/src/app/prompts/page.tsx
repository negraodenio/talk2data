import { Terminal, ShieldAlert, Cpu } from "lucide-react";

export default function PromptsPage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-amber-500" />
          <span className="text-sm font-medium text-zinc-300">Prompt Engineering</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-4xl mx-auto space-y-12 pb-20">
          
          <section className="space-y-4">
            <h1 className="text-3xl font-bold tracking-tight text-white mb-6">The Hybrid Orchestrator</h1>
            <p className="text-lg text-zinc-400 leading-relaxed">
              Standard AI Agents either fetch from SQL <em>or</em> Vector DBs, but rarely fuse them gracefully. 
              Our Custom Python Backend acts as a two-stage <strong>Hybrid Orchestrator</strong> using system prompt engineering.
            </p>
          </section>

          <section className="space-y-6">
            <h2 className="text-xl font-semibold text-zinc-200 border-b border-zinc-800 pb-2">Stage 1: Safe Text-to-SQL</h2>
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 space-y-4">
              <div className="flex items-center gap-3 mb-2">
                <ShieldAlert className="w-5 h-5 text-rose-400" />
                <h3 className="font-semibold text-white">Preventing SQL Injections</h3>
              </div>
              <p className="text-zinc-400 text-sm leading-relaxed mb-4">
                Instead of blindly asking an LLM to generate raw <code>SELECT * FROM...</code> queries (which exposes the backend to Prompt Injection and massive hallucination risks), we use a systemic Guardrail Prompt:
              </p>
              <div className="bg-black/50 p-4 rounded-xl font-mono text-sm text-amber-200/80 border border-zinc-800/80">
                "Analyze the following question: '...'. Extract ONLY the company name or financial ticker mentioned. If none is mentioned, answer 'NONE'."
              </div>
              <p className="text-zinc-400 text-sm leading-relaxed mt-4">
                The Python backend then securely sanitizes this entity and uses standard ORM methods (<code>ilike</code>) against Supabase.
              </p>
            </div>
          </section>

          <section className="space-y-6">
            <h2 className="text-xl font-semibold text-zinc-200 border-b border-zinc-800 pb-2">Stage 2: The Final Synthesis</h2>
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 space-y-4">
              <div className="flex items-center gap-3 mb-2">
                <Cpu className="w-5 h-5 text-emerald-400" />
                <h3 className="font-semibold text-white">Dynamic Context Injection</h3>
              </div>
              <p className="text-zinc-400 text-sm leading-relaxed mb-4">
                Once we have the raw SQL row (e.g., Apple's target price) AND the raw Semantic Chunks (e.g., geopolitical macro risks), we inject both into a strict synthesis prompt.
              </p>
              <div className="bg-black/50 p-4 rounded-xl font-mono text-sm text-emerald-300/80 border border-zinc-800/80 space-y-2">
                <p>Dynamically Extracted Context: &#123;context_text&#125;</p>
                <p className="mt-4 pt-4 border-t border-zinc-800 text-rose-300/80">
                  Critical Rules:<br/>
                  1. You MUST answer ONLY using the provided Extracted Context. Do not invent financial math...<br/>
                  2. If there is not enough information... firmly declare: "I do not have enough information"<br/>
                  3. YOUR FINAL RESPONSE MUST ALWAYS BE 100% IN ENGLISH.
                </p>
              </div>
            </div>
          </section>

        </div>
      </div>
    </>
  );
}
