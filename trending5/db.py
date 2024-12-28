from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["stir_marketplace"]
    return db
