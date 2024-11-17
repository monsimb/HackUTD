import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Sample data: phrases indicating an intent to buy or refinance a home
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
print(f"Accuracy: {accuracy:.2f}")

# Function to predict the intent of a new sentence
def predict_intent(text):
    return model.predict([text])[0]

# Test the intention detector with new sentences
test_sentences = [
    "I'm looking to buy a new house next year.",
    "How do I refinance my mortgage?",
    "Can you help me get a loan to buy a home?",
    "I want to lower my monthly mortgage payments.",
    "I am considering refinancing my current home loan.",
    "Do you offer home purchase loans?",
    "I'm planning to refinance my mortgage soon.",
    "What's the process to buy a house?",
    "I need help with refinancing my home."
]

for sentence in test_sentences:
    intent = predict_intent(sentence)
    print(f"Sentence: '{sentence}'\nPredicted Intent: {intent}\n")
