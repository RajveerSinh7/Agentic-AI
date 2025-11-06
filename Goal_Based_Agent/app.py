from langchain_mistralai import ChatMistralAI
from langchain.agents.react.agent import create_react_agent
from langchain.agents import AgentExecutor
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain import hub
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Initialize Mistral model
llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0,
    api_key=os.getenv("MISTRAL_API_KEY")
)

# Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Application info dictionary
application_info = {
    "name": None,
    "email": None,
    "skills": None
}

# Extract info from user input
def extract_application_info(text: str) -> str:
    name_match = re.search(r"(?:my name is|i am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text, re.IGNORECASE)
    email_match = re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", text)
    skills_match = re.search(r"(?:skills are|i know |i can use)\s+(.+)", text, re.IGNORECASE)

    response = []

    if name_match:
        application_info["name"] = name_match.group(1).title()
        response.append("Name saved!")

    if email_match:
        application_info["email"] = email_match.group(0)
        response.append("Email saved!")

    if skills_match:
        application_info["skills"] = skills_match.group(1).strip()
        response.append("Skills saved!")

    if not any([name_match, email_match, skills_match]):
        return "❌ I couldn’t find any info! Please provide your name, email, and skills."

    return " ".join(response) + " Let me check what else I need."

# Check goal completion
def check_application_goal(_: str) -> str:
    if all(application_info.values()):
        return f"✅ You're ready! Name: {application_info['name']}, Email: {application_info['email']}, Skills: {application_info['skills']}"
    else:
        missing = [k for k, v in application_info.items() if not v]
        return f"Still need: {', '.join(missing)}. Please provide these."

# Tools
tools = [
    Tool(
        name="extract_application_info",
        func=extract_application_info,
        description="Extracts user's name, email, and skills from text."
    ),
    Tool(
        name="check_application_goal",
        func=check_application_goal,
        description="Checks if all required details are provided.",
        return_direct=True
    )
]

# Pull the standard ReAct prompt
react_prompt = hub.pull("hwchase17/react")

# Customize by prepending your system instructions to the system template
system_content = """You are a job application assistant. 
Your goal is to collect the user's name, email, and skills.
Use the tools provided to extract this information and check whether all required data is collected.
Once everything is collected, inform the user that application info is complete and stop.

"""
react_prompt.messages[0].prompt.template = system_content + react_prompt.messages[0].prompt.template

# Create the ReAct agent
agent = create_react_agent(llm, tools, react_prompt)

# Create executor
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    memory=memory, 
    handle_parsing_errors=True
)

# Chat loop
print("👋 Hi, I am your job application assistant. Please tell me your name, email, and skills.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Bye! Good luck!")
        break

    response = agent_executor.invoke({"input": user_input})
    print("Bot:", response["output"])

    if "you're ready" in response["output"].lower():
        print("✅ Application info complete!")
        break