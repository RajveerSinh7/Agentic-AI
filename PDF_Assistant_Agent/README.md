# PDF Recipe Assistant

An AI-powered assistant that answers questions about Thai recipes from a PDF menu. It uses **Phi AI** for autonomous assistant capabilities, **PostgreSQL** with **pgvector** for vector storage, and a local HuggingFace embedder for embeddings. Groq LLM is used for chat responses.

---

## Features

- Load knowledge from PDF URLs into a vector database.
- Store and retrieve chat history in PostgreSQL.
- Use Groq LLM for fast, accurate question-answering.
- Local embeddings with HuggingFace sentence-transformers model.
- CLI-based interface for interactive chat.

---

## Requirements

- Python 3.12+
- PostgreSQL (local server)
- Required Python packages (install in a virtual environment):

```bash
pip install typer python-dotenv phi pypdf psycopg[binary] sentence-transformers
