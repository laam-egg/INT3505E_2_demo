import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/soa_demo')
client = MongoClient(MONGO_URL)
db = client.get_database()

# Collections
patrons_collection = db.patrons
titles_collection = db.titles
copies_collection = db.copies
borrows_collection = db.borrows

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

def get_copy_status(copy_id):
    """Determine copy status based on latest borrow"""
    # Find all borrows for this copy
    copy_borrows = list(borrows_collection.find({"copy_id": copy_id}))
    
    if not copy_borrows:
        return "AVAILABLE"
    
    # Find latest borrow by statusLastUpdatedAt
    latest_borrow = max(copy_borrows, key=lambda x: x["statusLastUpdatedAt"])
    
    if latest_borrow["status"] == "BORROWING":
        return "BORROWED"
    elif latest_borrow["status"] == "LOST":
        return "LOST"
    else:  # RETURNED
        return "AVAILABLE"

# Helper functions for common operations
def str_to_objectid(id_str):
    """Convert string ID to ObjectId if valid, otherwise return None"""
    try:
        return ObjectId(id_str)
    except:
        return None

def get_title_with_stats(title_doc):
    """Add copy statistics to title document"""
    if title_doc is None:
        return None
    
    title_id = str(title_doc['_id'])
    
    # Get all copies for this title
    copies = list(copies_collection.find({"title_id": title_id}))
    
    total_copies = len(copies)
    available_count = 0
    borrowed_count = 0
    lost_count = 0
    
    for copy in copies:
        copy_id = str(copy['_id'])
        status = get_copy_status(copy_id)
        
        if status == "AVAILABLE":
            available_count += 1
        elif status == "BORROWED":
            borrowed_count += 1
        elif status == "LOST":
            lost_count += 1
    
    # Serialize and add stats
    result = serialize_mongo_doc(title_doc)
    result.update({
        'totalCopies': total_copies,
        'availableCopies': available_count,
        'borrowedCopies': borrowed_count,
        'lostCopies': lost_count
    })
    
    return result