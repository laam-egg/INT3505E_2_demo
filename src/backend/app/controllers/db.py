from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URL from environment or use default
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/soa_demo')

# Initialize MongoDB client and database
client = MongoClient(MONGO_URL)
db = client.get_default_database()

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
        return [serialize_mongo_doc(d) for d in doc]
    
    result = {}
    for key, value in doc.items():
        if key == '_id':
            result['id'] = str(value)
        elif isinstance(value, ObjectId):
            result[key] = str(value)
        else:
            result[key] = value
    return result

def str_to_objectid(id_str):
    """Convert string ID to ObjectId"""
    try:
        return ObjectId(id_str)
    except:
        return None

def get_copy_status(copy_id):
    """Determine copy status based on latest borrow"""
    copy_borrows = list(borrows_collection.find({"copy_id": copy_id}))
    if not copy_borrows:
        return "AVAILABLE"
    
    # Sort by statusLastUpdatedAt and get the latest
    latest_borrow = max(copy_borrows, key=lambda x: x["statusLastUpdatedAt"])
    
    if latest_borrow["status"] == "BORROWING":
        return "BORROWED"
    elif latest_borrow["status"] == "LOST":
        return "LOST"
    else:  # RETURNED
        return "AVAILABLE"

def get_title_with_stats(title):
    """Get title with copy statistics"""
    title_id = str(title["_id"])
    copies = list(copies_collection.find({"title_id": title_id}))
    
    total_copies = len(copies)
    available_count = 0
    borrowed_count = 0
    lost_count = 0
    
    for copy in copies:
        copy_id = str(copy["_id"])
        status = get_copy_status(copy_id)
        if status == "AVAILABLE":
            available_count += 1
        elif status == "BORROWED":
            borrowed_count += 1
        elif status == "LOST":
            lost_count += 1
    
    result = serialize_mongo_doc(title)
    result.update({
        "totalCopies": total_copies,
        "availableCopies": available_count,
        "borrowedCopies": borrowed_count,
        "lostCopies": lost_count
    })
    
    return result