# GenAI Capital: Live Interview Demo Script

This document provides a structured path for presenting your GenAI Investment Assistant during the technical interview. It is designed to proactively answer the interviewers' unasked questions and demonstrate how your architecture gracefully handles the "gotchas" typical of this coding challenge.

---

## 🎭 The Setup (What to say first)
*“For this GenAI assistant, instead of relying on opaque frameworks like LangChain, I built a custom **Hybrid Orchestrator** in Python (FastAPI). It connects to a single unified PostgreSQL database (Supabase) that serves as both the Relational DB (for the CSV equities data) and the Vector DB (using `pgvector` for the PDFs).*

*To showcase the final product, I also built a premium Next.js frontend with Supabase Auth readiness. Let's test its intelligence by throwing three distinct scenarios at it.”*

---

## 🟢 Scenario 1: The Exact Match (Structured Data / Text-to-SQL)
Interviewers want to see if your LLM can reliably fetch numerical data from the CSV without hallucinating.

**🗣️ You type:**
> *"What is the current price and target price of Microsoft?"*

**Expected Behavior:**
- The Hybrid Orchestrator extracts the entity `"Microsoft"`.
- It executes a relational `ILIKE` query to the Supabase `equities` table.
- **The Wow Factor:** The UI instantly returns the exact math without inventing decimal points. The bottom of the chat bubble explicitly displays the source tag!

---

## 🔵 Scenario 2: Semantic PDF Search (Unstructured Data / RAG)
Interviewers want to test your vector embeddings and chunking strategy.

**🗣️ You type:**
> *"According to the OECD Economic Outlook, what are the primary risks to global GDP growth in 2025?"*

**Expected Behavior:**
- The Orchestrator's Entity Extractor finds no specific company, so it bypasses the SQL lookup.
- It embeds the prompt via OpenRouter and searches the `documents` table via Cosine Similarity (`pgvector`).
- **The Wow Factor:** The LLM reads the exact PDF chunks retrieved and formulates a cohesive summary.

---

## 🔴 Scenario 3: The "Gotcha" (The True Hybrid Query)
This is the critical test. Basic LLM agents usually fail here—they either use the SQL tool OR the RAG tool, but rarely combine them correctly.

**🗣️ You type:**
> *"What is the target price of Apple, and how could the geopolitical instability mentioned in the global macro reports affect its corresponding sector?"*

**Expected Behavior:**
- **Our Orchestrator's Brilliance:** It extracts `"Apple"` and fetches the SQL data. *Concurrently*, it performs the semantic vector search for "geopolitical instability" across the 7 PDFs. 
- It fuses BOTH contexts (Relational Data Table + PDF Text Chunks) into a strict dynamic context window.
- **The Wow Factor:** The assistant replies accurately with the Apple stock math *and* merges it with the macroeconomic risk analysis. The UI Source badge will display **"Híbrido (SQL + RAG vetorial)"**, proving to the interviewers that the cross-pollination of data worked seamlessly.

---

## 🛡️ Scenario 4: The Hallucination Guardrail (Another Gotcha)
Interviewers often try to trick the LLM into answering something it shouldn't know, or asking for a stock that was NOT in the CSV.

**🗣️ You type:**
> *"What is the exact target price for Tesla?"* *(Assuming Tesla is NOT in your test equities.xlsx, or pick a fictional company like 'StarkIndustries')*

**Expected Behavior:**
- The SQL query returns empty.
- **The Wow Factor:** Instead of hallucinating a random stock price from its internal OpenAI training data, the assistant respects our strict custom Python prompt rules and replies: *"The data is not available in our internal sources."*
- This proves to the interviewers that your system is Enterprise-ready and protects against financial hallucinations.
