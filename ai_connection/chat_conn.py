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

load_dotenv()

# API reference using SambaNova
client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

# Home Purchase and Refinancing Intent Detection Model
data = [
    ("I want to buy a house", "buy"),
    ("Looking for a mortgage to purchase a home", "buy"),
    ("I am interested in buying a new home", "buy"),
    ("Can I get a loan for a house?", "buy"),
    ("I am thinking about refinancing my mortgage", "refinance"),
    ("I need to lower my mortgage rate", "refinance"),
    ("Is it a good time to refinance my home?", "refinance"),
    ("How can I refinance my home loan?", "refinance"),
    ("I want to sell my house and buy a new one", "buy"),
    ("I need to get a better rate on my mortgage", "refinance"),
    ("Looking to refinance my home loan", "refinance"),
    ("I'm ready to purchase a new house", "buy"),
    ("Can I refinance my mortgage to pay off debts?", "refinance"),
    ("How do I start the process of buying a house?", "buy"),
    ("Refinancing my home is my top priority now", "refinance"),
]

# Split data into texts and labels
texts = [item[0] for item in data]
labels = [item[1] for item in data]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Create a text classification pipeline with a vectorizer and logistic regression
model = make_pipeline(CountVectorizer(), LogisticRegression())

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Intent Detection Accuracy: {accuracy:.2f}")

# Function to predict the intent of a new sentence
def predict_intent(text):
    return model.predict([text])[0]

# Tool to handle home purchase and refinancing related queries
@tool
def calculate_home_loan(loan_amount: float, interest_rate: float, loan_term: int) -> float:
    """
    Calculate the monthly payment for a home loan using the loan amount,
    interest rate, and loan term.
    """
    monthly_interest_rate = interest_rate / 12 / 100
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
            st.write("It looks like you're asking about buying a home. Let's talk about Home Purchase.")
            loan_amount = st.number_input("Enter loan amount:", min_value=0.0, value=200000.0)
            interest_rate = st.number_input("Enter interest rate (%):", min_value=0.0, value=3.5)
            loan_term = st.number_input("Enter loan term (years):", min_value=1, value=30)
            
            if loan_amount and interest_rate and loan_term:
                monthly_payment = calculate_home_loan.invoke(input={"loan_amount": loan_amount, "interest_rate": interest_rate, "loan_term": loan_term})
                st.write(f"Your estimated monthly payment is: ${monthly_payment:.2f}")

        elif predicted_intent == "refinance":
            st.write("It looks like you're asking about refinancing. Let's talk about Refinancing.")
            current_loan_balance = st.number_input("Enter current loan balance:", min_value=0.0, value=150000.0)
            current_interest_rate = st.number_input("Enter current interest rate (%):", min_value=0.0, value=4.0)
            new_interest_rate = st.number_input("Enter new interest rate (%):", min_value=0.0, value=3.0)
            
            if current_loan_balance and current_interest_rate and new_interest_rate:
                monthly_savings = refinancing_calculator(current_loan_balance, current_interest_rate, new_interest_rate)
                st.write(f"Your estimated monthly savings from refinancing would be: ${monthly_savings:.2f}")
        
        # Handle chat functionality
        st_chat(user_input)


if __name__ == "__main__":
    main()
