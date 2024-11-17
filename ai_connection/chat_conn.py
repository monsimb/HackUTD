# Python program to handle chat functionality

import os
from typing import Annotated, TypedDict
import openai
from dotenv import load_dotenv
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain.tools import tool, StructuredTool
import formulas
from pymongo import MongoClient

load_dotenv()

MONGO_URI='mongodb+srv://{USER}:{PASS}@hackutd-project-dev-clu.n76pi.mongodb.net/'

client = MongoClient(MONGO_URI)
db = client["mortgage"]
users_coll = db["buy"]

# API reference using SambaNova
client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

# Get user data's principal and num_payments data
def get_user_data(_id):
    """
    Fetches user data from MongoDB on user ID
    """
    _id = users_coll.find_one({"_id": _id})
    if _id:
        return{
            "principal": _id.get("principal"),
            "payments": _id.get("payments")
        }
    return None

# response = client.chat.completions.create(
#     model='Meta-Llama-3.1-8B-Instruct',
#     messages=[{"role": "system", "content": "You are a helpful assistant"},
#               {"role": "user", "content": "Hello"}],
#     temperature=0.1,
#     top_p=0.1
# )

# print(response.choices[0].message.content)



@tool
def NAME(word: str) -> float:
    """
    Triggers 
    Returns 
    """

@tool
def BUY(user_id: str) -> str:
    """
    Use the user's Principal interest, Interest rate, and Number of payments
    to find out the monthly payment
    """
    # get their PN from DB
    user_data = get_user_data(user_id)
    if not user_data:
        return "User data not found."
    
    prin = user_data["principal"]
    payments = user_data["payments"]
    # interest = API_CALL_HERE
    interest = 2

    # Try to get calculate the monthly payment
    try:
        payment = formulas.M(prin, interest, payments)
        return f'Monthly mortgage payment: ${payment: .2f}'
    except Exception as e:
        return f'Error occurred: {e}'
    

@tool
def monthly_payment(principal: float, interest_rate: float, num_payments: int) -> float:
    return formulas.M(principal, interest_rate, num_payments)

# Route 1: Buy
def buying_agent(state, agent, name):
    last_message = state['messages'][-1]
    if "mortgage" in last_message.content.lower():
        user_id = last_message.get("_id")
        result = agent.tools["BUY"].invoke({"_id": user_id})
        return result
    return "Mortgage keyword not mentioned. No action taken."

# Route 2: Refinance
def refinance_agent(state, agent, name):
    return "Refinance agent triggered"


class AgentState(TypedDict):    # Agent's current state, it can be history of messsages and other attributes you want to maintain
    messages: Annotated[list[AnyMessage], operator.add]   # {'messages': []}


# Agents. Handles the tools
class Agent:
    def __init__(self, model, tools, system=""):
        self.model = model
        self.system
        self.tools = {t.name: t for t in tools}

    def exists_action(self, state: AgentState):
        # Checks for specific msg tool name
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_llm(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}  # AIMessage

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling Tool: {t}")
            if not t['name'] in self.tools:  # check for bad tool name from LLM
                print(f"\n Tool: {t} does not exist.")
                result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Tools Execution Complete. Back to the model!")
        return {'messages': results}    # [ToolMessage, ToolMessage, ...]


tools = [
    NAME,
    BUY,
    monthly_payment,
    refinance_agent,
    buying_agent,
]