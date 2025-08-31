# Intro to Vector DBs — Ingestão e RAG com LangChain, Pinecone, HF e Groq

Projeto didático para ingestão de texto em Pinecone e consulta via RAG usando LangChain.

Visão geral
- Ingestão (`ingestion.py`): carrega `mediumblog1.txt`, fatia em chunks, gera embeddings (Hugging Face) e faz upsert no Pinecone.
- Consulta (`main.py`): recupera do Pinecone e responde com um LLM Groq (ChatGroq) usando um prompt simples.

Arquivos principais
- `ingestion.py`: pipeline de ingestão (load → split → embed → upsert Pinecone).
- `main.py`: exemplo RAG mínimo (retriever Pinecone + ChatGroq + PromptTemplate).
- `mediumblog1.txt`: texto de exemplo.
- `.env`: variáveis de ambiente (não versionar segredos reais).
- `Pipfile` / `Pipfile.lock`: dependências (Pipenv).

Pré‑requisitos
- Python 3.10
- Conta Pinecone com índice criado (dimensão correta)
- Token da Hugging Face Inference API
- Chave de API da Groq (para `main.py`)

Instalação
- Pipenv:
  - `pipenv install`
- venv + pip (alternativa):
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -U langchain langchain-pinecone langchain-huggingface langchain-groq langchainhub python-dotenv langchain-text-splitters langchain-community`

Configuração (.env)
- Hugging Face:
  - `HUGGINGFACEHUB_API_TOKEN=...`
  - `HF_EMBED_MODEL=BAAI/bge-large-en-v1.5` (opcional; padrão no código)
- Pinecone:
  - `PINECONE_API_KEY=...`
  - `PINECONE_INDEX=...`
- Groq (LLM para `main.py`):
  - `GROQ_API_KEY=...`
  - `GROQ_LLM_MODEL=llama-3.1-8b-instant` (opcional)
- LangSmith (opcional; tracing no `ingestion.py`):
  - `LANGSMITH_API_KEY=...`
  - `LANGSMITH_PROJECT=intro-to-vector-dbs` (opcional)

Índice no Pinecone (dimensionalidade)
- Modelo padrão `BAAI/bge-large-en-v1.5` → 1024 dimensões.
- Crie seu índice com `dimension=1024`. Se trocar o modelo, ajuste a dimensão.

Execução
- Ingestão (popular o índice):
  - Pipenv: `pipenv run python ingestion.py`
  - venv: `python ingestion.py`
- Consulta (RAG simples):
  - Pipenv: `pipenv run python main.py`
  - venv: `python main.py`

Como funciona (`main.py`)
- Usa `HuggingFaceEndpointEmbeddings` para embeddar consultas com o mesmo modelo da ingestão.
- Cria `PineconeVectorStore` e `retriever` a partir do índice.
- Define um `PromptTemplate` simples e usa `ChatGroq` para responder com base no contexto recuperado.
- Imprime a resposta e as fontes (quando disponíveis).

Solução de problemas
- Autenticação: verifique `.env` (HF, Pinecone, Groq). Sem `GROQ_API_KEY`, o `ChatGroq` falha.
- Dimensionalidade do índice: deve casar com o modelo de embeddings (ex.: 1024 para `BAAI/bge-large-en-v1.5`).
- Taxas/limites HF: considere reduzir chamadas ou ajustar plano.
- Dependências: se faltar um pacote, instale conforme a seção “Instalação”.

Avisos
- Não commite `.env` com segredos reais.
- Projeto focado em simplicidade e didática.

Referências
- LangChain: https://python.langchain.com/
- Pinecone: https://www.pinecone.io/
- Hugging Face Inference: https://huggingface.co/inference-api
- Groq: https://console.groq.com/

Licença
Projeto sob MIT License. Veja `LICENSE`.
