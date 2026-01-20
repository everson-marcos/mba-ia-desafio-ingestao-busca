import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector

load_dotenv()

# Valida se todas as variáveis de ambiente foram carregadas
for k in ("OPENAI_API_KEY", "DATABASE_URL", "PDF_PATH", "PG_VECTOR_COLLECTION_NAME"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} not found.");

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt():
   embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))
   
   store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True
    )
   
   llm = ChatOpenAI(
        model=os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano"),
        temperature=0
    )
   
   def search(question):
    results = store.similarity_search_with_score(question, k=10)

    if not results:
        return "Sem resultados."

    contexto = ""
    for result in results:
        contexto += result[0].page_content.strip() + "\n"

    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)
    response = llm.invoke(prompt)
    return response.content.strip()

   return search