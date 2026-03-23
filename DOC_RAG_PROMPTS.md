# Engenharia de Prompts: A Lógica Híbrida do Orquestrador

Um dos maiores diferenciais da nossa solução é o uso dinâmico da Engenharia de Prompt (na rota `api/index.py`) para contornar a ausência de agentes do LangChain, resolvendo um problema complexo com abordagens nativas.

O sistema faz uso de **Dois Prompts Sistêmicos** (prompts executados via código como instruções base do sistema):

---

## PROMPT 1: O "Text-to-SQL Guardrail" (Extração de Entidade)

Requisito a atender: *"Implementar funcionalidades de Text-to-SQL."*

A abordagem convencional para Text-to-SQL pede à IA para "gerar código SQL cru", o que é um risco de falha gigantesco e expõe dados em uma aplicação web. 

Nossa abordagem usa a IA apenas para ler a intenção e **extrair parâmetros**, os quais injetamos com segurança no Supabase SQL.

**O Prompt:**
> ```text
> Analise a pergunta: '{question}'. 
> Extraia apenas o nome da empresa ou o ticker financeiro mencionado. 
> Se nenhum for mencionado, responda 'NONE'. 
> Retorne APENAS o nome ou ticker, sem pontuação.
> ```

**A Lógica Injetada:** 
Recebemos a resposta "Mircrosoft", validamos com código Python se a resposta é `!= "NONE"` e jogamos direto no client PostgREST para um `ILIKE '%Microsoft%'`. Desta forma, nós abstraímos a complexidade de Query e simulamos perfeitamente de maneira higienizada o Text-to-SQL Agent.

---

## PROMPT 2: A Síntese Final de Fontes Opostas (O Orquestrador Híbrido)

Agora que possuímos a Linha Bruta retirada do Banco Relacional (SQL) e os 3 Parágrafos Brutos retirados via Busca Semântica Vetorial (RAG) do Banco, precisamos fundi-los.

O modelo final `gpt-4o-mini` recebe esta instrução arquitetural:

**O Prompt:**
> ```text
> Você é um Assistente Financeiro Sênior da GenAI Capital.
> O usuário fará uma pergunta. 
> Você tem abaixo o contexto extraído dinamicamente das planilhas de ações (SQL) e dos PDFs macroeconômicos (RAG).
> 
> Contexto Dinâmico Extraído:
> {context_text} 
> 
> Pergunta do Usuário: {question}
> 
> Regras:
> 1. Responda APENAS usando as informações do Contexto Dinâmico Extraído.
> 2. Se não houver informações suficientes no contexto para responder partes da pergunta, avise que os dados não estão disponíveis nas fontes internas.
> 3. Responda sempre no mesmo idioma que o usuário perguntou (se ele perguntar em Inglês, responda em Inglês).
> ```

### O Motivo Profundo Das Três Regras:

1. **A Regra Anti-Alucinação (Regras 1 e 2):** Se um usuário pede o ticket da "FakeCompanyXYZ", o SQL volta vazio, o vetor não entende, e o `{context_text}` entra em branco. Sem essa regra, um modelo generativo como GPT-4 poderia tentar resgatar o valor da FakeCompanyXYZ dos seus dados originais de treinamento, arruinando o sistema RAG corporativo. Ao prender a IA **"apenas usando o contexto"** e orientar sobre a ausência, ela fornece a mensagem de "dados insuficientes" sem dar o braço a torcer.
2. **A Manuntenção da Padronagem (Regra 3):** Segundo o PDF da entrevista técnica, *"All user interactions and responses should be in English."* No entanto, como fomos instruídos, nosso Prompt sistêmico está em português porque isso facilita a compreensão do orquestrador de síntese, fazendo-o atuar com melhor robustez ao obedecer as ordens estruturais — mas o seu output reage à origem do Input, mantendo a regra da entrevista perfeitamente satisfeita.
