import os
import pymongo
from dotenv import load_dotenv
import pymongo.errors

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)
db = client['mortgage']
people_collection = db['people']
buy_collection = db['buy']

def get_user_data(username):
    """Check if a user exists in the database."""
    return people_collection.find_one({"username": username})

def add_user_data(user_data):
    """Add a new user to the database."""
    try:
        # Use username as the document ID
        user_data["username"] = user_data.pop("_id")
        people_collection.insert_one(user_data)
        return True
    except pymongo.errors.DuplicateKeyError:
        return False

# Alternative to form on Welcome page -> should store prompted answers from chat in DB
def add_chat_data(chat_data):
    """Add the user form information received from the chat"""
    try:
        # Use username as document ID
        chat_data["username"] = chat_data.pop("_id")
        buy_collection.insert_one(chat_data)
        return True
    except pymongo.errors.DuplicateKeyError:
        return False