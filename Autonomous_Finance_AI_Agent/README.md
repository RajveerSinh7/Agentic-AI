# Autonomous AI Agents Playground

This project demonstrates an **AI agent playground** using [Phi](https://github.com/phi-xyz/phi), integrating **Mistral LLMs** with tools like **DuckDuckGo** and **Yahoo Finance**. Users can interact with multiple AI agents through a web-based interface.

---

## Features

1. **Web Search Agent**
   - Uses **Mistral LLM**.
   - Can search the web via **DuckDuckGo**.
   - Returns sources along with answers.

2. **Finance AI Agent**
   - Uses **Mistral LLM**.
   - Uses **Yahoo Finance Tools** to fetch:
     - Stock prices
     - Analyst recommendations
     - Company info
     - Company news
     - Key financial ratios
   - Displays results in tables.

3. **Playground Interface**
   - Run multiple agents interactively.
   - Web-based UI served locally.
   - Real-time API endpoints powered by **FastAPI** (under the hood).

---

## Project Structure

```
.
├── main.py                 # Main script to launch the playground
├── .env                    # Environment file containing Mistral API key
└── README.md
```

---

## Requirements

- Python 3.12+
- Phi (`pip install phi`)
- python-dotenv (`pip install python-dotenv`)
- FastAPI, Uvicorn (installed automatically with Phi)
- Other dependencies are handled by Phi and `dotenv`.

---

## Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. **Create a virtual environment and activate**
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Mistral API key**
   - Create a `.env` file in the project root:
```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

---

## Running the Playground

```bash
python main.py
```

- The server will start at: `http://localhost:7777`.
- Access the web-based playground to interact with your AI agents.

---

## Code Overview

- **Patch for Python 3.12+**:  
  Ensures `inspect.getargspec()` works for compatibility with older code.

- **Agents**
  - `web_search_agent` uses DuckDuckGo for web queries.
  - `finance_agent` uses YFinanceTools for financial data.

- **Playground**
  - `Playground(agents=[...]).get_app()` returns a FastAPI app.
  - `serve_playground_app("playground:app", reload=True)` runs the web server.

- **Streaming**
  - Currently set to `stream=False`. If enabled, agents would stream responses (if supported by the model).

---

## Usage Example

- Ask the **Web Search Agent**:
  > "Latest news on AI regulations 2025"

- Ask the **Finance Agent**:
  > "Get stock price and analyst rating for TSLA"

Results are displayed in the playground interface with proper formatting.

---

## Notes

- Phi internally uses **FastAPI** for HTTP endpoints.
- Uvicorn serves the FastAPI app in development mode.
- Ensure the Mistral API key is valid and has required access.

---

## License

MIT License

