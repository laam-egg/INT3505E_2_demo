from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')

if not MONGO_URL:
    print(f"Environment variable MONGO_URL is missing.")
    import sys
    sys.exit(1)

client = MongoClient(MONGO_URL)
db = client.get_default_database()

webhooks_collection = db.webhooks
# Create compound index for webhooks: UNIQUE for pairs of (targetUrl, eventName)
webhooks_collection.create_index([("targetUrl", 1), ("eventName", 1)], unique=True)
# Create index for eventName to facilitate search
webhooks_collection.create_index("eventName")
# Also create index for targetUrl to facilitate search
webhooks_collection.create_index("targetUrl")

def serialize_mongo_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    
    if isinstance(doc, list):
        return [serialize_mongo_doc(item) for item in doc]
    
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if key == '_id':
                result['id'] = str(value)  # Convert ObjectId to string
            elif isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = serialize_mongo_doc(value)
            elif isinstance(value, list):
                result[key] = serialize_mongo_doc(value)
            else:
                result[key] = value
        return result
    
    return doc

def str_to_objectid(id_str):
    """Convert string ID to ObjectId"""
    try:
        return ObjectId(id_str)
    except:
        return None
