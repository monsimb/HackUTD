# Python program to handle chat functionality

import os
from typing import Annotated, TypedDict
import openai
from dotenv import load_dotenv
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain.tools import tool, StructuredTool
import formulas

load_dotenv()

# API reference using SambaNova
client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

# response = client.chat.completions.create(
#     model='Meta-Llama-3.1-8B-Instruct',
#     messages=[{"role": "system", "content": "You are a helpful assistant"},
#               {"role": "user", "content": "Hello"}],
#     temperature=0.1,
#     top_p=0.1
# )

# print(response.choices[0].message.content)



# @tool
# def NAME(word: str) -> float:
#     """
#     Triggers 
#     Returns 
#     """





class AgentState(TypedDict):    # Agent's current state, it can be history of messsages and other attributes you want to maintain
    messages: Annotated[list[AnyMessage], operator.add]   # {'messages': []}


# Agents. Handles the tools
class Agent:
    def __init__(self, model, tools, system=""):
        self.system
        self.tools = {t.name: t for t in tools}

    def exists_action(self, state: AgentState):
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


