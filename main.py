import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

load_dotenv()

if __name__ == '__main__':
    # Exemplo simples de RAG: consulta -> recupera do Pinecone -> responde com Groq
    query = "O que é Pinecone em machine learning?"

    # 1) Variáveis mínimas
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    pinecone_index = os.getenv("PINECONE_INDEX")
    groq_key = os.getenv("GROQ_API_KEY")
    missing = [n for n, v in {
        "HUGGINGFACEHUB_API_TOKEN": hf_token,
        "PINECONE_INDEX": pinecone_index,
        "GROQ_API_KEY": groq_key,
    }.items() if not v]
    if missing:
        raise SystemExit(f"Defina no .env: {', '.join(missing)}")

    # 2) Embeddings (Hugging Face Inference API)
    embeddings = HuggingFaceEndpointEmbeddings(
        huggingfacehub_api_token=hf_token,
        model=os.getenv("HF_EMBED_MODEL", "BAAI/bge-large-en-v1.5"),
    )

    # 3) LLM (Groq)
    llm = ChatGroq(model=os.getenv("GROQ_LLM_MODEL", "llama-3.1-8b-instant"))

    # 4) Vector Store (Pinecone) e Retriever
    vectorstore = PineconeVectorStore(index_name=pinecone_index, embedding=embeddings)
    retriever = vectorstore.as_retriever()

    # 5) Cadeia de recuperação com prompt básico
    prompt = PromptTemplate.from_template(
        (
            "Use o contexto para responder de forma breve e correta.\n\n"
            "Contexto:\n{context}\n\nPergunta: {input}"
        )
    )
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    # 6) Consultar e exibir resposta + fontes
    result = retrieval_chain.invoke({"input": query})
    print("Resposta:\n", result.get("answer"))
    if result.get("context"):
        print("\nFontes:")
        for i, doc in enumerate(result["context"], start=1):
            src = (doc.metadata or {}).get("source") or (doc.metadata or {}).get("id") or "desconhecida"
            print(f"{i}. {src}")
