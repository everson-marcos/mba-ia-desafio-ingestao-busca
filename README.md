# 📄 Projeto RAG – Ingestão e Chat com PDF

Este projeto implementa uma solução **RAG (Retrieval-Augmented Generation)** utilizando **LangChain**, **PostgreSQL + PGVector** e **LLMs**, permitindo a ingestão de documentos PDF e a realização de perguntas via chat com base no conteúdo ingerido.

---

## 🧠 Visão Geral da Arquitetura

Fluxo simplificado da solução:

1. PDF é carregado
2. Conteúdo é dividido em *chunks*
3. Embeddings são gerados
4. Embeddings são armazenados no PostgreSQL (PGVector)
5. O chat consulta o banco vetorial
6. O contexto recuperado é usado para gerar a resposta

---

## 🚀 Pré-requisitos

- **Docker** e **Docker Compose**
- **Python 3.10+** (recomendado evitar versões experimentais como 3.14)
- **pip**
- **venv**

---

## 🐘 1. Subir o banco de dados (PostgreSQL + PGVector)

Inicie os containers definidos no `docker-compose.yml`:

```bash
docker compose up -d
```

## Configurar o ambiente Python
```bash
python3 -m venv venv
```

## Ative o ambiente:
```bash
source venv/bin/activate
```

## Instale as dependências:
```bash
pip install \
  langchain \
  langchain-openai \
  langchain-google-genai \
  langchain-community \
  langchain-text-splitters \
  langchain-postgres \
  "psycopg[binary]" \
  python-dotenv \
  beautifulsoup4 \
  pypdf
```

## Gere o arquivo de dependências:
```bash
pip freeze > requirements.txt
```

## Configurar variáveis de ambiente
```bash
OPENAI_API_KEY=seu_token_aqui
OPENAI_MODEL=text-embedding-3-small
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=pdf_documents

```

## Executar a ingestão do PDF
```bash
python src/ingest.py
```

## Executar o chat
```bash
python src/chat.py
```