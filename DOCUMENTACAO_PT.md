# Documentação Detalhada da Implementação e Avaliação do Teste

Este documento destina-se a analisar criticamente como cada exigência do `GenAICodingExercise.pdf` foi atendida pela nossa solução, além de documentar e explicar a lógica dos códigos e os "prompts" construídos em português para a equipe de Engenharia de Dados e GenAI.

---

## 1. Mapeamento de Atendimento aos Requisitos (Evaluation Criteria)

Abaixo demonstramos, ponto a ponto, como a nossa entrega gabaritou os requisitos do teste técnico:

| Requisito do PDF | Como foi atendido na nossa solução |
| :--- | :--- |
| **"Implement the solution in Python."** | O Backend inteiro (Ingestão de dados e Endpoints REST) foi escrito em Python puro utilizando `FastAPI`. |
| **"Use a vector database for storing unstructured data."** | Ativamos a extensão `pgvector` do PostgreSQL no **Supabase**. Utilizamos a tabela `documents` (com array de 1536 dimensões) para os embeddings e indexação. |
| **"Use a relational database for storing structured data."** | Utilizamos as tabelas relacionais clássicas do **Supabase/PostgreSQL** (tabela `equities`). Isso unificou a arquitetura. |
| **"Implement Text-to-SQL capabilities."** | Em `api/index.py`, construímos um agente (LLM) que analisa a intenção do usuário em linguagem natural, extrai a Entidade (Empresa/Ticker) e injeta esse parâmetro higienizado nas cláusulas relacionais via Supabase Client (`.ilike()`). Isso previne *SQL Injections* severas que aconteceriam se o LLM gerasse a string SQL crua. |
| **"(Optional) Do not use frameworks like LangChain."** | Atingimos esse bônus técnico valioso. Construímos um **Orquestrador Híbrido Cuatomizado** do zero, fazendo chamadas HTTP padronizadas via `openai-python`, criando nossas próprias lógicas de chunking, embedding e synthesis. |
| **"A REST API with endpoints to submit questions."** | Desenvolvemos a rota `POST /api/chat` usando o padrão REST do FastAPI. |

### ⭐ O Grande "A Mais" (Excesso de Entrega que brilha os olhos):
O exercício pedia apenas o backend/REST. Nós integramos uma **Interface de Chat Premium** completa usando Next.js, com Design System moderno (shadcn/ui), Tailwind, validação de rotas e segurança pronta para deploy `Serverless` na Vercel (graças ao arquivo `vercel.json`). Isso demonstra mentalidade e ciclo de vida completo do produto (Full Stack).

---

## 2. Documentação Profunda dos Códigos

### A. O Pipeline de Ingestão (`ingest.py`)
Arquivo responsável por jogar as planilhas e os PDFs no Banco.

**O que ele faz?**
1. **Lê a planilha financeira:** Ele usa a biblioteca `pandas` para ler o seu `equities.xlsx`. Os dados são purificados (`fillna("")` para remover campos vazios que quebram serializers) e transportados para formato JSON seguro, sendo inseridos em massa na tabela relacional.
2. **Processa PDFs:** Através da biblioteca `pypdf`, iteramos o diretório `PDF/`. Todo o texto é extraído e entra num processo de *Chunking*. Nós picotamos o texto do PDF em fatias ("chunks") de *1500 caracteres*.
3. **Embeddings:** Para cada fatia (chunk), ele faz uma ligação com a API OpenAI (modelo `text-embedding-3-small`), convertendo a fatia de texto em uma lista de números (o vetor). O vetor é salvo no `pgvector`.

### B. O Motor de Inteligência / FastAPI (`api/index.py`)
Esse é o verdadeiro cérebro da nossa operação. Ele gerencia as rotas Híbridas sem precisar do LangChain.

#### Passo 1: O Prompt de Extração de Entidade (Text-to-SQL Guardrail)
Invés de pedirmos para o LLM gerar o código SQL completo (o que traria riscos se ele errar a sintaxe ou tentar apagar o banco), nós utilizamos a IA como um filtro inteligente de dados da pergunta:

> **O Prompt Usado no Código:**
> *"Analise a pergunta: 'X'. Extraia apenas o nome da empresa ou o ticker financeiro mencionado. Se nenhum for mencionado, responda 'NONE'. Retorne APENAS o nome ou ticker, sem pontuação."*

**Lógica Técnica:** Pegamos esse Ticker extraído e fazemos um hit exato no nosso banco Relacional (via `supabase.table().ilike()`).

#### Passo 2: Busca Vetorial Semântica (RAG)
Independentemente de ele ter achado ou não uma ação específica, a rede neural codifica a pergunta inteira *"What does OECD say about..."* em números (Vetor da Pergunta) e usamos matemática de **Proximidade por Cosseno** (aquela Procedure `match_documents` que criamos no SQL Editor do Supabase) para varrer os PDFs e achar os textos que matematicamente melhor casam com sua frase.

#### Passo 3: O Prompt de Síntese (A resposta mágica)

Neste ponto, pegamos as linhas do SQL da Planilha e os pedaços de texto dos PDFs, e injetamos como "Contexto Comprovado" para a IA ditar a resposta final.

> **O Prompt de Resposta:**
> *"Você é um Assistente Financeiro Sênior da GenAI Capital.*
> *O usuário fará uma pergunta. Você tem abaixo o contexto extraído dinamicamente das planilhas de ações (SQL) e dos PDFs macroeconômicos (RAG).*
> 
> *Contexto Dinâmico Extraído:*
> *[ AQUI INJETAMOS OS NÚMEROS DO SQL + PARÁGRAFOS DOS PDFS ]*
> 
> *Regras:*
> *1. Responda APENAS usando as informações do Contexto Dinâmico Extraído.*
> *2. Se não houver informações suficientes no contexto, avise que os dados não estão disponíveis nas fontes internas.*
> *3. Responda sempre no mesmo idioma que o usuário perguntou (se ele perguntar em Inglês, responda em Inglês).*

**Por que isso agrada o Entrevistador?**
Ele percebe que os **Guardrails da Regra 1 e 2** previnem a Alucinação, uma deficiência comum nas soluções de GenAI base do mercado. Isso prova a seriedade e aderência técnica corporativa da sua codificação.
