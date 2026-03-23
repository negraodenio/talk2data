# RAG + pgvector: O Código Por Trás da Busca Semântica

Este documento detalha tecnicamente como implementamos a Retrieval-Augmented Generation (RAG) combinada com a busca semântica vetorial no Supabase (`pgvector`), sem depender do LangChain. Essa é a arquitetura exata do nosso código escrito em Python.

---

## 1. O Banco de Dados (`schema.sql`)
O "motor" de tudo começa no Banco. Para fazer busca semântica (achar ideias e não palavras exatas), ativamos a extensão matemática `vector`.

```sql
create extension if not exists vector;
```

Em seguida, criamos a tabela `documents` com a coluna `embedding` configurada para armazenar um array de **1536 dimensões** (que é o tamanho exato da saída do modelo de Embedding da OpenAI `text-embedding-3-small`).

### A Matemática: `match_documents` (Stored Procedure)
Nós criamos uma função no PostgreSQL que aceita a `query_embedding` (a pergunta do usuário transformada em números) e calcula a **Distância por Cosseno** (`<=>`) entre a pergunta e todos os PDFs armazenados.
```sql
create or replace function match_documents (
  query_embedding vector(1536),
  match_count int default null
) returns table (
  id bigint,
  content text,
  similarity float
)
-- Retorna os PDFs ordenados do maior casamento semântico (menor distância) para o menor.
```

---

## 2. A Injeção de Dados (`ingest.py`)

Como o PDF gigante vira "inteligência" de busca?
A função `ingest_pdfs()` faz três coisas primárias:

### A) Leitura e Chunking (Picotando o Texto)
Um PDF de Macros tem 50 páginas. A IA não pode ler tudo de uma vez. Nós programamos em puro Python uma rotina para extrair o texto via `pypdf` e depois fazer um **Chunking de 1500 caracteres** com 200 de overlap (sobreposição). O *Overlap* impede que uma frase importante seja cortada no meio.

### B) Geração de Embeddings
Para cada bloco (chunk) de 1500 caracteres, chamamos a OpenAI (passando pela OpenRouter):
```python
res = client.embeddings.create(
    input=chunk, 
    model="openai/text-embedding-3-small"
)
vector = res.data[0].embedding # O Array de 1536 números surge aqui.
```

### C) Supabase Insert
Cada bloco de texto e seu respectivo vertor de 1536 números é gravado no banco de dados.

---

## 3. O Servidor de RAG (`api/index.py`)
Quando o usuário digita: *"What are the geopolitical risks globally?"*, o que acontece?

**1º Passo: Converter a Pergunta do Usuário**
A máquina não consegue pesquisar a palavra "risk". Precisamos converter a pergunta em vetor usando o mesmo modelo de Embedding que usamos na ingestão (`text-embedding-3-small`).
```python
res = client.embeddings.create(
    input=question, 
    model="openai/text-embedding-3-small"
)
query_embedding = res.data[0].embedding
```

**2º Passo: Executar a Busca por Proximidade Semântica (Cosine Similarity)**
Conectamos via REST ao Supabase e executamos a função matemática `match_documents` que criamos lá atrás, pedindo os **3 parágrafos limitrofes** (`match_count: 3`) mais próximos matematicamente da pergunta do usuário.
```python
response = supabase.rpc("match_documents", {
    "query_embedding": query_embedding, 
    "match_count": 3
}).execute()
```

**3º Passo: Concatenação**
Extraímos o `content` (o texto literal original em inglês contido no BD) dos 3 resultados, unimos em uma string e a injetamos no Prompt Final da IA, caracterizando o Padrão Ouro de RAG!
