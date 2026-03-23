import { ShieldCheck, AlertTriangle, Lock, Crosshair } from "lucide-react";

export default function GuardrailsPage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-rose-500" />
          <span className="text-sm font-medium text-zinc-300">Security & Guardrails</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-4xl mx-auto space-y-12 pb-20">
          
          <section className="space-y-4">
            <h1 className="text-3xl font-bold tracking-tight text-white mb-6 flex items-center gap-3">
              Powerful Hallucination Prevention
            </h1>
            <p className="text-lg text-zinc-400 leading-relaxed border-l-4 border-rose-500/50 pl-4">
              In financial applications, generative AI <strong>must never guess</strong>. If data is not present in the primary sources, the AI must fail gracefully. We built three layers of systemic Guardrails to prevent mathematical and factual hallucinations.
            </p>
          </section>

          <div className="space-y-6 mt-8">
            {/* Guardrail 1 */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
                <AlertTriangle className="w-24 h-24 text-amber-500" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 text-xs">1</span>
                The "Strict Grounding" Policy
              </h3>
              <p className="text-zinc-400 text-sm leading-relaxed mt-4 w-3/4">
                The final synthesis prompt mathematically restricts the LLM from accessing its predefined <code>GPT-4</code> weights for financial data. The prompt explicitly orders:
              </p>
              <div className="bg-black/50 p-4 rounded-xl font-mono text-xs text-amber-300/80 border border-zinc-800/80 mt-4 max-w-2xl relative z-10 hidden md:block">
                "You MUST answer ONLY using the provided Extracted Context. Do not invent financial math or prices from your own knowledge."
              </div>
            </div>

            {/* Guardrail 2 */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
                <Lock className="w-24 h-24 text-rose-500" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-rose-500/20 text-rose-400 text-xs">2</span>
                Sanitized Entity Extraction (Anti-SQL Injection)
              </h3>
              <p className="text-zinc-400 text-sm leading-relaxed mt-4 w-3/4">
                Instead of allowing the LLM to write raw <code>SQL</code> code directly to the Supabase database (which introduces massive security flaws and SQL Injection vulnerabilities), the Python backend uses the LLM <em>solely</em> to extract the Entity Name. 
              </p>
              <p className="text-zinc-400 text-sm leading-relaxed mt-2 w-3/4">
                The extracted string is then safely passed to Supabase's native ORM via a parameterized Python <code>ilike()</code> query.
              </p>
            </div>

            {/* Guardrail 3 */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
                <Crosshair className="w-32 h-32 text-indigo-500" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-indigo-500/20 text-indigo-400 text-xs">3</span>
                The "Data Not Available" Fallback
              </h3>
              <p className="text-zinc-400 text-sm leading-relaxed mt-4 w-3/4">
                If the user asks for the price of a fictional company (e.g. <em>"Stark Industries"</em>) or a company whose region was not ingested (e.g. <em>"Where is Marks &amp; Spencer from?"</em>), the SQL database returns empty.
                The LLM reads an empty context block and triggers the systemic fallback rule, gracefully replying:
              </p>
              <div className="bg-black/50 p-4 rounded-xl font-mono text-xs text-indigo-300/80 border border-zinc-800/80 mt-4 max-w-2xl relative z-10">
                "I do not have enough information available in the internal sources to answer this."
              </div>
            </div>
          </div>

        </div>
      </div>
    </>
  );
}
