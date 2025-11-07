import inspect

# Patch for Python 3.12+ (to run getargspec() in current py version)
if not hasattr(inspect, 'getargspec'):
    from collections import namedtuple
    ArgSpec = namedtuple('ArgSpec', 'args varargs keywords defaults')

    def getargspec(func):
        return ArgSpec(*inspect.getfullargspec(func)[:4])
    inspect.getargspec = getargspec

# --- Now safe to import phi and others ---
import os
from dotenv import load_dotenv

from phi.agent import Agent
from phi.app import *
from phi.model.mistral import MistralChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.playground import Playground, serve_playground_app

# Load environment variables
load_dotenv()

# ✅ Set your Mistral API key
mistral_api_key = os.getenv("MISTRAL_API_KEY")

if not mistral_api_key:
    raise ValueError("❌ MISTRAL_API_KEY not found in .env file")

# --- Agents ---
# 1) websearch agent using duckduckgo
web_search_agent = Agent(
    name="Web Search Agent",
    role="search the web for information",
    model=MistralChat(id="mistral-large", api_key=mistral_api_key),
    tools=[DuckDuckGo()],
    instructions=["Always include sources."],
    show_tool_calls=True,
    markdown=True,
    stream=False
)

# 2) finance agent with yahoo finance tool
finance_agent = Agent(
    name="Finance AI Agent",
    model=MistralChat(id="mistral-large", api_key=mistral_api_key),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
            key_financial_ratios=True,
        )
    ],
    instructions=["Use tables to display data."],
    show_tool_calls=True,
    markdown=True,
    stream=False
)

# Playground setup
app = Playground(agents=[finance_agent, web_search_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)