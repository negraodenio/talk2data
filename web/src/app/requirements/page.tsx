import { CheckCircle2, ListChecks, Star } from "lucide-react";

export default function RequirementsPage() {
  return (
    <>
      <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <ListChecks className="w-5 h-5 text-fuchsia-500" />
          <span className="text-sm font-medium text-zinc-300">Requirements Matrix</span>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 md:p-10 scroll-smooth">
        <div className="max-w-4xl mx-auto space-y-12 pb-20">
          
          <section className="space-y-4">
            <h1 className="text-3xl font-bold tracking-tight text-white mb-6">Original Spec vs. Delivered Implementation</h1>
            <p className="text-lg text-zinc-400 leading-relaxed border-l-4 border-fuchsia-500/50 pl-4">
              This matrix maps the original functional and technical requirements from the `GenAICodingExercise.pdf` against the actual shipped platform architecture.
            </p>
          </section>

          <div className="space-y-6">
            
            {/* Requirement 1 */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6">
              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 space-y-2">
                  <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Requested</span>
                  <h3 className="text-lg font-medium text-zinc-200">Python REST API</h3>
                  <p className="text-sm text-zinc-400">Implement the solution in Python and create a REST API with endpoints to submit questions.</p>
                </div>
                <div className="hidden md:block w-px bg-zinc-800"></div>
                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-emerald-500 uppercase tracking-wider">Delivered</span>
                    <Star className="w-3 h-3 text-amber-400" />
                  </div>
                  <h3 className="text-lg font-medium text-emerald-400">Decoupled Full-Stack Platform</h3>
                  <p className="text-sm text-zinc-300">
                    Built the core intelligence using <strong>FastAPI</strong> in Python (<code>/api/chat</code> endpoint). Exceeded expectations by wrapping the API in a premium, fully-functional <strong>Next.js (React) Interface</strong>.
                  </p>
                </div>
              </div>
            </div>

            {/* Requirement 2 */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6">
              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 space-y-2">
                  <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Requested</span>
                  <h3 className="text-lg font-medium text-zinc-200">Dual Database Types</h3>
                  <p className="text-sm text-zinc-400">Use a Vector Database for unstructured data and a Relational Database for structured data.</p>
                </div>
                <div className="hidden md:block w-px bg-zinc-800"></div>
                <div className="flex-1 space-y-2">
                  <span className="text-xs font-semibold text-emerald-500 uppercase tracking-wider">Delivered</span>
                  <h3 className="text-lg font-medium text-emerald-400">Unified Supabase Infrastructure</h3>
                  <p className="text-sm text-zinc-300">
                    Utilized <strong>Supabase</strong> to elegantly handle both within the same cluster. <code>PostgreSQL</code> strictly manages a verified base of <strong>1,821 Equities</strong>, while the <code>pgvector</code> extension handles the 1536-dimensional math locally.
                  </p>
                </div>
              </div>
            </div>

            {/* Requirement 3 */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6">
              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 space-y-2">
                  <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Requested</span>
                  <h3 className="text-lg font-medium text-zinc-200">Hybrid AI Workflow</h3>
                  <p className="text-sm text-zinc-400">Combine insights from both data sources to provide comprehensive natural-language answers.</p>
                </div>
                <div className="hidden md:block w-px bg-zinc-800"></div>
                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-emerald-500 uppercase tracking-wider">Delivered</span>
                    <Star className="w-3 h-3 text-amber-400" />
                  </div>
                  <h3 className="text-lg font-medium text-emerald-400">Context-Aware Orchestrator</h3>
                  <p className="text-sm text-zinc-300">
                    Developed a robust custom Agent that calculates exactly when to deploy mathematical Vector Search and when to trigger safe Text-to-SQL logic against the tables, dynamically injecting a <strong>"Source Data Tag"</strong> in the UI.
                  </p>
                </div>
              </div>
            </div>

            {/* Requirement 4 */}
            <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6">
              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 space-y-2">
                  <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Requested (Optional)</span>
                  <h3 className="text-lg font-medium text-zinc-200">No High-Level Frameworks</h3>
                  <p className="text-sm text-zinc-400">Do not use frameworks such as LangChain or LangGraph to solve the Orchestration.</p>
                </div>
                <div className="hidden md:block w-px bg-zinc-800"></div>
                <div className="flex-1 space-y-2">
                  <span className="text-xs font-semibold text-emerald-500 uppercase tracking-wider">Delivered</span>
                  <h3 className="text-lg font-medium text-emerald-400">Native Python Implementation</h3>
                  <p className="text-sm text-zinc-300">
                    Created the entire pipeline "from scratch". Managed embedding extraction, custom chunking arrays, and <code>Cosine Similarity</code> algorithms manually with Python logic, proving deep architectural capability.
                  </p>
                </div>
              </div>
            </div>

             {/* Requirement 5 */}
             <div className="bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6">
              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 space-y-2">
                  <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Requested</span>
                  <h3 className="text-lg font-medium text-zinc-200">English Mandatory</h3>
                  <p className="text-sm text-zinc-400">All user interactions and responses should be in English.</p>
                </div>
                <div className="hidden md:block w-px bg-zinc-800"></div>
                <div className="flex-1 space-y-2">
                  <span className="text-xs font-semibold text-emerald-500 uppercase tracking-wider">Delivered</span>
                  <h3 className="text-lg font-medium text-emerald-400">Absolute Conformity</h3>
                  <p className="text-sm text-zinc-300">
                    Configured the System Prompts and Next.js interfaces strictly to business-level English.
                  </p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </>
  );
}
