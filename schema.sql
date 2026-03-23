-- 1. Habilitar extensão de vetores (para RAG)
create extension if not exists vector;

-- 2. Tabela para os dados da planilha (Estruturado)
CREATE TABLE equities (
  id SERIAL PRIMARY KEY,
  ticker TEXT,
  name TEXT,
  sector TEXT,
  asset_class TEXT,
  market_value REAL,
  price REAL
  -- Adicione/ajuste colunas conforme o seu equities.xlsx
);

-- 3. Tabela para os PDFs (Não Estruturado/Vetorial)
CREATE TABLE documents (
  id BIGSERIAL PRIMARY KEY,
  content TEXT,
  metadata JSONB,
  embedding VECTOR(1536) -- Tamanho para o modelo text-embedding-3-small da OpenAI
);

-- 4. Função para buscar similaridade (RAG)
create or replace function match_documents(query_embedding vector(1536), match_count int)
returns table (id bigint, content text, metadata jsonb, similarity float)
language plpgsql
as $$ begin
  return query
  select
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;
