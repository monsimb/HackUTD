import os
import pymongo
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)
db = client['mortgage']
people_collection = db['people']

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
