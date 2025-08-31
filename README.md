# Intro to Vector DBs — Ingestão com LangChain e Pinecone

Projeto simples para demonstrar ingestão de texto, divisão em chunks, geração de embeddings e upsert em um índice Pinecone usando LangChain. Este repositório faz parte do curso “LangChain” na Udemy: https://www.udemy.com/course/langchain

## Visão Geral
- Carrega um texto de `mediumblog1.txt`.
- Divide o conteúdo em chunks com sobreposição.
- Gera embeddings via Hugging Face Inference API.
- Faz upsert dos vetores em um índice no Pinecone.

Arquivos principais:
- `ingestion.py`: script de ingestão (carrega, fatia, embeda e envia ao Pinecone).
- `mediumblog1.txt`: texto de exemplo para ingestão.
- `.env`: variáveis de ambiente (não versionar com segredos reais).
- `Pipfile` / `Pipfile.lock`: dependências via Pipenv.

## Pré‑requisitos
- Python 3.10
- Pipenv
- Conta no Pinecone e um índice criado com a dimensão correta (ver abaixo)
- Token da Hugging Face Inference API

## Instalação
1) Instale dependências (usando o lock, se preferir):
```bash
pipenv install
# Se necessário para o embeddings endpoint:
pipenv install langchain-huggingface
```

2) (Opcional) Ative o shell do ambiente:
```bash
pipenv shell
```

## Configuração (.env)
Crie um arquivo `.env` na raiz do projeto com as chaves necessárias:
```bash
HUGGINGFACEHUB_API_TOKEN=seu_token_hf
PINECONE_API_KEY=sua_chave_pinecone
PINECONE_INDEX=nome_do_indice
# Opcional: modelo de embeddings na HF Inference API (padrão: BAAI/bge-large-en-v1.5)
HF_EMBED_MODEL=BAAI/bge-large-en-v1.5
```
- O script utiliza `HuggingFaceEndpointEmbeddings`, portanto é necessário um token de Inference API válido.
- Garanta que o índice Pinecone informado em `PINECONE_INDEX` exista previamente.

## Índice no Pinecone (dimensionalidade)
- O modelo padrão `BAAI/bge-large-en-v1.5` produz embeddings de 1024 dimensões.
- Crie o índice no Pinecone com `dimension = 1024` (e demais configs conforme sua conta/região).
- Se alterar o modelo, ajuste a dimensão do índice para corresponder ao modelo escolhido.

## Execução
Para rodar a ingestão:
```bash
pipenv run python ingestion.py
```
Saída esperada (exemplo):
```
Ingestão simples: carregar texto -> gerar embeddings -> enviar ao Pinecone
Carregando documento...
Fatiando em chunks...
Gerando embeddings com o modelo: BAAI/bge-large-en-v1.5
Enviando N chunks para o índice 'seu_indice' no Pinecone...
Pronto! Upsert concluído no Pinecone.
```

## Ajustes comuns
- Mudar o arquivo de entrada: edite o caminho em `ingestion.py` (loader aponta para `mediumblog1.txt`).
- Tamanho/overlap dos chunks: ajuste `chunk_size` e `chunk_overlap` no `CharacterTextSplitter`.
- Modelo de embeddings: defina `HF_EMBED_MODEL` no `.env`.

## Solução de Problemas
- ImportError para `langchain_huggingface`: instale a integração explicitamente:
  ```bash
  pipenv install langchain-huggingface
  ```
- Erro de dimensionalidade no Pinecone: verifique se a dimensão do índice coincide com a do modelo (ex.: 1024 para `BAAI/bge-large-en-v1.5`).
- Falha de autenticação (HF ou Pinecone): confira o `.env` e evite caracteres extras/espacos.
- Rate limiting na Hugging Face: aguarde ou use um plano compatível; reduza a taxa de chamadas.

## Avisos
- Não commite seu arquivo `.env` com segredos reais.
- Este projeto é didático e simplificado para fins do curso.

## Referências
- Curso Udemy (módulos sobre ingestão e vetores): https://www.udemy.com/course/langchain
- LangChain: https://python.langchain.com/
- Pinecone: https://www.pinecone.io/
- Hugging Face Inference: https://huggingface.co/inference-api

## Licença
Este projeto é licenciado sob a MIT License. Consulte `LICENSE` para detalhes.
