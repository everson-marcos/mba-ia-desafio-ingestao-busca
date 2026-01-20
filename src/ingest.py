import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

# Valida se todas as variáveis de ambiente foram carregadas
for k in ("OPENAI_API_KEY", "OPENAI_EMBEDDING_MODEL", "DATABASE_URL", "PDF_PATH", "PG_VECTOR_COLLECTION_NAME"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} not found.");

current_dir = Path(__file__).parent.parent
pdf_path = current_dir / os.getenv("PDF_PATH")

docs = PyPDFLoader(str(pdf_path)).load()

splits = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    add_start_index=False,
).split_documents(docs)

if not splits:
    raise SystemExit("Nenhum documento foi carregado.")


enriched =[
    Document(
        page_content=doc.page_content,
        metadata={k: v for k, v in doc.metadata.items() if v not in ("", None)}
    ) for doc in splits
]

# Cria os indices
ids = [f"doc-{i}" for i in range(len(enriched))]

embeddings = OpenAIEmbeddings(
    model=os.getenv("OPENAI_MODEL", "text-embedding-3-small")
)

# Prepara a conexão
store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True
)

# Adiciona no banco
store.add_documents(documents=enriched, ids=ids)