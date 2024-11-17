import os
import streamlit as st
from typing import Annotated, TypedDict
import openai
from dotenv import load_dotenv
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain.tools import tool, StructuredTool
from .api_calls import mortgage_rate

load_dotenv()

# API reference using SambaNova
client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

# Function to predict the intent of a new sentence
def predict_intent(model, text):
    return model.predict([text])[0]

# Tool to calculate the monthly payment for home loan
@tool
def calculate_home_loan(loan_amount: float, yr: float, loan_term: int) -> float:
    """
    Calculate the monthly payment for a home loan using the loan amount,
    interest rate, and loan term.
    """
    switch = {
        '15': 0,
        '30': 1
    }
    current_rate = mortgage_rate()[switch.get(yr)]  # Use the 15-year rate or another option

    monthly_interest_rate = current_rate / 12 / 100  # Convert annual rate to monthly
    num_payments = loan_term * 12
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)

    return monthly_payment

@tool
def refinancing_calculator(current_loan_balance: float, current_interest_rate: float, new_interest_rate: float, loan_term: int) -> float:
    """
    Compare old and new monthly payments to calculate the savings per month.
    """
    old_monthly_payment = current_loan_balance * current_interest_rate / 12 / 100
    new_monthly_payment = current_loan_balance * new_interest_rate / 12 / 100
    return old_monthly_payment - new_monthly_payment

@tool
def break_even_calculator(refinancing_savings_per_month: float, refinancing_costs: float) -> float:
    """
    Calculate the break-even point (in months) for refinancing based on savings per month and refinancing costs.
    """
    if refinancing_savings_per_month <= 0:
        return float('inf')  # If there's no savings, the break-even point is infinite
    return refinancing_costs / refinancing_savings_per_month


# Agent State for managing message history
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


# Agent class for managing the flow and tool invocations
class Agent:
    def __init__(self, model, tools, system=""):
        self.system = system
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
            if t['name'] not in self.tools:
                result = "Incorrect Tool Name, Please Retry."
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        return {'messages': results}    # [ToolMessage, ToolMessage, ...]

def st_chat(prompt: str, injection:str =""):
    """Handles chat flow with the assistant."""
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Concatenate conversation history into a single prompt string
    conversation_history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
    full_prompt = f"{conversation_history}\nUser: {prompt}\nAssistant:" + injection

    # Call the assistant's model (this can be OpenAI or another service)
    response = client.chat.completions.create(
        model='Meta-Llama-3.1-8B-Instruct',
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.1,
        top_p=0.1
    )

    # Display the assistant's message
    st.chat_message("assistant").write(response.choices[0].message.content)
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

# Function to handle user input and ask for loan details for refinancing
def handle_refinancing(state: AgentState):
    st.chat_message("assistant").write("It looks like you're asking about refinancing. Let's talk about Refinancing.")
    
    # Fetch the current mortgage rates using the API
    mortgage_rates = mortgage_rate()
    fmr15 = mortgage_rates[0]
    fmr30 = mortgage_rates[1]

    # Display the rates to the user
    st.chat_message("assistant").write(f"The current mortgage rates are:\n- 15-Year Fixed: {fmr15}%\n- 30-Year Fixed: {fmr30}%\n")
    
    # Ask for current loan balance, current interest rate, and desired new rate
    st.chat_message("assistant").write("Can you provide your current loan balance and interest rate?")
    st.session_state.messages.append({"role": "assistant", "content": "Can you provide your current loan balance and interest rate?"})
    
    # Wait for user input and store data
    current_loan_balance = float(st.text_input("Current loan balance"))
    current_interest_rate = float(st.text_input("Current interest rate (in %)"))
    
    st.chat_message("assistant").write(f"Please provide the new interest rate you're considering for refinancing (you can choose from 15-year: {fmr15}% or 30-year: {fmr30}%)")
    new_interest_rate = float(st.text_input("New interest rate (in %)"))
    
    # Ask for loan term
    st.chat_message("assistant").write("What loan term are you considering for the refinance? (e.g., 15 years, 30 years)")
    loan_term = int(st.text_input("Loan term (in years)"))
    
    # Ask for refinancing costs (e.g., closing costs)
    st.chat_message("assistant").write("Are there any refinancing costs (like closing costs)? Please provide the amount.")
    refinancing_costs = float(st.text_input("Refinancing costs"))

    # Calculate the savings per month
    savings_per_month = refinancing_calculator(current_loan_balance, current_interest_rate, new_interest_rate, loan_term)
    
    # Calculate the break-even point
    break_even_months = break_even_calculator(savings_per_month, refinancing_costs)
    
    # Display results to the user
    st.chat_message("assistant").write(f"Your estimated savings per month from refinancing will be ${savings_per_month:.2f}.")
    st.chat_message("assistant").write(f"Based on your refinancing costs of ${refinancing_costs:.2f}, it will take approximately {break_even_months:.2f} months to break even on your refinancing.")

