import inspect

# Patch for Python 3.12+ (to run getargspec() in current py version)
if not hasattr(inspect, 'getargspec'):
    from collections import namedtuple
    ArgSpec = namedtuple('ArgSpec', 'args varargs keywords defaults')

    def getargspec(func):
        return ArgSpec(*inspect.getfullargspec(func)[:4])
    inspect.getargspec = getargspec

import typer  # for cli app
from typing import Optional, List
from phi.assistant import Assistant  # independent autonomous ai
from phi.storage.agent.postgres import PgAgentStorage  # correct path for agent storage
from phi.knowledge.pdf import PDFUrlKnowledgeBase  # to load pdfs
from phi.vectordb.pgvector import PgVector  # vector DB for knowledge base
from phi.llm.groq import Groq  # for Groq LLM backend
from phi.embedder.huggingface import HuggingfaceCustomEmbedder  # fixed: correct class name for local embedder (no API key)

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"  # database running locally

# Local embedder (free, no keys; uses sentence-transformers model)
embedder = HuggingfaceCustomEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")

# Creating a knowledge base
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],  # demo pdf (menu of thai dishes)
    vector_db=PgVector(table_name="recipes", db_url=db_url, embedder=embedder)  # pass embedder here
)
knowledge_base.load(recreate=True)  # recreate=True: Drops/recreates table to fix ID schema bug

# Setting up storage for chat history
storage = PgAgentStorage(table_name="pdf_assistant", db_url=db_url)

# Function to launch the assistant
def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None
    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]

    # Initialize the assistant
    assistant = Assistant(
        llm=Groq(model="llama3-8b-8192"),  # Groq for chat (fast)
        embedder=embedder,  # HuggingFace for embeddings (consistent with KB)
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        name="PDF Recipe Assistant",  # optional: gives it identity
        description="An assistant that answers questions about Thai recipes from the PDF menu.",  # optional
        # show tool calls in the response
        show_tool_calls=True,
        # enable the assistant to search knowledge base
        search_knowledge=True,
        # enable the assistant to read the chat history
        read_chat_history=True,
    )

    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    assistant.cli_app(markdown=True)

if __name__ == "__main__":
    typer.run(pdf_assistant)