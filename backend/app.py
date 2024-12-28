from pymongo import MongoClient
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Test MongoDB Connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["stir_marketplace"]

# List available collections
print("MongoDB connection successful. Collections:", db.list_collection_names())


proxy_uri = os.getenv("PROXYMESH_URI")

# Test Proxy Connection
try:
    response = requests.get("https://httpbin.org/ip", proxies={"http": proxy_uri, "https": proxy_uri})
    print("Proxy response:", response.json())
except Exception as e:
    print("Error using ProxyMesh:", e)
