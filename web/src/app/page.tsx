"use client";

import { useState, useRef, useEffect } from "react";
import { Send, TrendingUp, FileText, Database, Shield, Zap } from "lucide-react";

export default function ChatDashboard() {
  const [messages, setMessages] = useState<{ role: "user" | "assistant"; content: string; source?: string }[]>([
    {
      role: "assistant",
      content: "Hello! I am your Senior Investment Research Assistant. I can analyze macroeconomic PDFs and structured stock data. How can I help you today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setIsLoading(true);

    try {
      // Chamada para a API Python (FastAPI) na porta 8000 (ou mesma origem se deployado no Vercel)
      const apiUrl = process.env.NODE_ENV === "development" ? "http://127.0.0.1:8000/api/chat" : "/api/chat";
      
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg }),
      });
      
      const data = await response.json();
      
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer || "Desculpe, não consegui obter uma resposta.", source: data.source },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Erro ao conectar com o backend Python. Verifique se o FastAPI está rodando." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Header */}
        <header className="h-16 border-b border-zinc-800/50 flex items-center px-6 justify-between backdrop-blur-md sticky top-0 z-10">
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-400" />
            <span className="text-sm font-medium text-zinc-300">Investment Terminal</span>
          </div>
          <div className="flex items-center gap-3">
             <span className="px-3 py-1 text-xs rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-2">
               <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
               System Online
             </span>
          </div>
        </header>

        {/* Chat History */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-8 scroll-smooth">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
              <div className={`max-w-[75%] rounded-2xl px-5 py-4 ${
                msg.role === "user" 
                  ? "bg-emerald-600 text-white shadow-lg shadow-emerald-900/20" 
                  : "bg-zinc-900 border border-zinc-800 text-zinc-200"
              }`}>
                <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                {msg.source && (
                  <div className="mt-3 pt-3 border-t border-zinc-700/50 text-xs text-zinc-400 flex items-center gap-2">
                    <Database className="w-3 h-3" />
                    Source: {msg.source}
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start animate-in fade-in">
              <div className="bg-zinc-900 border border-zinc-800 rounded-2xl px-5 py-4 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-zinc-500 animate-bounce"></span>
                <span className="w-2 h-2 rounded-full bg-zinc-500 animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                <span className="w-2 h-2 rounded-full bg-zinc-500 animate-bounce" style={{ animationDelay: '0.4s' }}></span>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-6 pt-2 bg-gradient-to-t from-[#0a0a0a] to-transparent">
          <div className="max-w-4xl mx-auto relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-emerald-600 to-cyan-600 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
            <div className="relative flex items-center">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder="Ask about macroeconomic trends or specific equities..."
                className="w-full bg-zinc-900/90 border border-zinc-800 text-zinc-100 rounded-2xl py-4 pl-5 pr-14 focus:outline-none focus:ring-1 focus:ring-emerald-500/50 placeholder:text-zinc-600 shadow-xl"
              />
              <button 
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
                className="absolute right-2 p-2 rounded-xl bg-emerald-600 text-white hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            <p className="text-center text-[10px] text-zinc-600 mt-3 flex items-center justify-center gap-1">
              Data protected by Supabase RLS. Model powered by OpenRouter.
            </p>
          </div>
        </div>

    </>
  );
}
