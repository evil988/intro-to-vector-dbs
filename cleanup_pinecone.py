"""
Script didático: limpa TODOS os vetores do índice Pinecone
configurado no .env. Opcionalmente, você pode definir um namespace.

Passos:
1) Ler .env (PINECONE_API_KEY e PINECONE_INDEX)
2) Conectar ao índice
3) Deletar todos os vetores (com ou sem namespace)

Observações:
- Para limpar apenas um namespace, ajuste a variável NAMESPACE abaixo.
- Para apagar o índice inteiro (e não só os vetores), veja o bloco
  comentado no final do arquivo.
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Opcional: coloque aqui o namespace que deseja limpar.
# Deixe como None para limpar todos os vetores do índice (todas as namespaces).
NAMESPACE = None  # ex.: "meu_namespace"


def main() -> None:
    # 1) Ler variáveis do .env
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX") or os.getenv("PINECONE_INDEX_NAME")
    if not api_key or not index_name:
        raise SystemExit("Defina PINECONE_API_KEY e PINECONE_INDEX no .env")

    # 2) Conectar ao Pinecone e ao índice
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    # 3) Deletar todos os vetores
    if NAMESPACE:
        print(f"Limpando todos os vetores do índice '{index_name}' no namespace '{NAMESPACE}'...")
        index.delete(delete_all=True, namespace=NAMESPACE)
    else:
        print(f"Limpando todos os vetores do índice '{index_name}' (todas as namespaces)...")
        index.delete(delete_all=True)

    print("Pronto! Vetores removidos com sucesso.")


if __name__ == "__main__":
    main()

# ------------------------------------------------------------
# DICA (opcional, destrutivo): apagar o índice inteiro.
# Descomente as linhas abaixo para apagar o índice ao invés de
# apenas limpar os vetores. USE COM CUIDADO!
#
#    pc = Pinecone(api_key=api_key)
#    print(f"Apagando índice '{index_name}'...")
#    pc.delete_index(index_name)
#    print("Índice apagado.")

