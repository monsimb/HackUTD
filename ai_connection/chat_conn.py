import os
import streamlit as st
from typing import Annotated, TypedDict
import openai
from dotenv import load_dotenv
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain.tools import tool, StructuredTool
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
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

# Tool to handle home purchase and refinancing related queries
@tool
def calculate_home_loan(loan_amount: float, interest_rate: float, loan_term: int) -> float:
    """
    Calculate the monthly payment for a home loan using the loan amount,
    interest rate, and loan term.
    """
    monthly_interest_rate = float(mortgage_rate()[0]) / 12 / 100
    num_payments = loan_term * 12
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    return monthly_payment


# Placeholder tools for refinancing
@tool
def refinancing_calculator(current_loan_balance: float, current_interest_rate: float, new_interest_rate: float) -> float:
    """
    Simple refinancing calculator: compares old and new rates for monthly payment difference.
    """
    # Example refinancing calculation logic (simplified)
    old_monthly_payment = current_loan_balance * current_interest_rate / 12 / 100
    new_monthly_payment = current_loan_balance * new_interest_rate / 12 / 100
    return new_monthly_payment - old_monthly_payment


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

def st_chat(prompt):
    """Handles chat flow with the assistant."""
    if prompt:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})  # Add to history
        
        # Concatenate conversation history into a single prompt string
        conversation_history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
        full_prompt = f"{conversation_history}\nUser: {prompt}\nAssistant:"

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

# Function to display the chat and ask user questions about home purchase or refinancing
def main():
    # Initialize Streamlit session state for chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Chatbot logic to handle further conversation
    user_input = st.text_input("Type your message here...")
    
    if user_input:
        # Predict intent using the trained model
        predicted_intent = predict_intent(user_input)

        if predicted_intent == "buy":
            # Chatbot asks user for details about buying a home
            with st.chat_message("assistant"):
                st.write("It looks like you're asking about buying a home. Let's talk about Home Purchase.")
                st.write("What is the loan amount you are considering?")
            # st_chat("What is the loan amount you are considering?")
        
        elif predicted_intent == "refinance":
            # Chatbot asks user for details about refinancing
            st.write("It looks like you're asking about refinancing. Let's talk about Refinancing.")
            st.session_state.messages.append({"role": "assistant", "content": "What is your current loan balance?"})
            st_chat("What is your current loan balance?")

        # Handle the next set of responses and proceed with the corresponding actions
        # These questions can be added dynamically based on user inputs and flow.
        
if __name__ == "__main__":
    main()
