import Link from "next/link";
import { TrendingUp, FileText, Database, Shield, LayoutDashboard, BrainCircuit, Terminal, Blocks, ListChecks, ShieldCheck } from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="w-72 border-r border-zinc-800/50 bg-[#0f0f11] p-6 flex flex-col hidden md:flex">
      <Link href="/" className="flex items-center gap-3 mb-10 hover:opacity-80 transition-opacity">
        <div className="p-2 bg-emerald-500/10 rounded-lg border border-emerald-500/20">
          <TrendingUp className="w-6 h-6 text-emerald-400" />
        </div>
        <div>
          <h1 className="text-sm font-semibold tracking-wide text-zinc-100">GenAI Capital</h1>
          <p className="text-xs text-zinc-500">Research Assistant</p>
        </div>
      </Link>

      <div className="space-y-8 flex-1">
        <div>
          <h2 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">Menu</h2>
          <div className="space-y-1">
            <Link href="/" className="flex items-center gap-3 text-sm text-zinc-400 hover:text-emerald-400 hover:bg-emerald-500/10 p-2 rounded-lg transition-colors">
              <LayoutDashboard className="w-4 h-4" />
              <span>Investment Chat</span>
            </Link>
          </div>
        </div>

        <div>
          <h2 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">Documentation</h2>
          <div className="space-y-1">
            <Link href="/architecture" className="flex items-center gap-3 text-sm text-zinc-400 hover:text-emerald-400 hover:bg-emerald-500/10 p-2 rounded-lg transition-colors">
              <Blocks className="w-4 h-4" />
              <span>System Architecture</span>
            </Link>
            <Link href="/spec" className="flex items-center gap-3 text-sm text-zinc-400 hover:text-emerald-400 hover:bg-emerald-500/10 p-2 rounded-lg transition-colors">
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
              <span>Technical Spec (PRD)</span>
            </Link>
            <Link href="/guardrails" className="flex items-center gap-3 text-sm text-zinc-400 hover:text-rose-400 hover:bg-rose-500/10 p-2 rounded-lg transition-colors">
              <Shield className="w-4 h-4" />
              <span>AI Guardrails</span>
            </Link>
            <Link href="/rag" className="flex items-center gap-3 text-sm text-zinc-400 hover:text-emerald-400 hover:bg-emerald-500/10 p-2 rounded-lg transition-colors">
              <Database className="w-4 h-4" />
              <span>Vector RAG Engine</span>
            </Link>
            <Link href="/prompts" className="flex items-center gap-3 text-sm text-zinc-400 hover:text-emerald-400 hover:bg-emerald-500/10 p-2 rounded-lg transition-colors">
              <Terminal className="w-4 h-4" />
              <span>Prompt Engineering</span>
            </Link>
            <Link href="/requirements" className="flex items-center gap-3 text-sm text-zinc-400 hover:text-fuchsia-400 hover:bg-fuchsia-500/10 p-2 rounded-lg transition-colors">
              <ListChecks className="w-4 h-4" />
              <span>Requirements Tracker</span>
            </Link>
            <Link href="/readme" className="flex items-center gap-3 text-sm text-zinc-400 hover:text-indigo-400 hover:bg-indigo-500/10 p-2 rounded-lg transition-colors">
              <FileText className="w-4 h-4" />
              <span>Main README</span>
            </Link>
            <Link href="/source-code" className="flex items-center gap-3 text-sm text-zinc-400 hover:text-cyan-400 hover:bg-cyan-500/10 p-2 rounded-lg transition-colors">
              <Terminal className="w-4 h-4" />
              <span>Python Source Code</span>
            </Link>
          </div>
        </div>
        
        <div>
          <h2 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">Stack</h2>
          <div className="space-y-2 p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/30 text-xs text-zinc-400">
            <div className="flex justify-between items-center"><span>Frontend</span><span className="text-zinc-300">Next.js 14</span></div>
            <div className="flex justify-between items-center"><span>Backend</span><span className="text-zinc-300">Python (FastAPI)</span></div>
            <div className="flex justify-between items-center"><span>Vector DB</span><span className="text-zinc-300">Supabase pgvector</span></div>
            <div className="flex justify-between items-center"><span>LLM</span><span className="text-zinc-300">GPT-4o mini</span></div>
          </div>
        </div>
      </div>
      
      <div className="mt-auto flex items-center gap-3 p-3 rounded-xl border border-zinc-800/50 bg-zinc-900/50">
        <Shield className="w-5 h-5 text-emerald-500" />
        <div className="text-xs">
          <p className="text-zinc-300 font-medium">Fully Secured</p>
          <p className="text-zinc-500">Python Guardrails</p>
        </div>
      </div>
    </aside>
  );
}
