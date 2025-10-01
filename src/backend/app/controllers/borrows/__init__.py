from ..common import Controller
from .dto.borrow import borrow_dto, borrow_create_dto, borrow_update_dto
from flask import request, jsonify
from flask_restx import abort
from datetime import datetime
from ..db import (patrons_collection, copies_collection, borrows_collection, 
                  serialize_mongo_doc, str_to_objectid, get_copy_status)

borrows_controller = Controller("borrows", __name__)

Borrow = borrow_dto(borrows_controller)
BorrowCreate = borrow_create_dto(borrows_controller)
BorrowUpdate = borrow_update_dto(borrows_controller)

parser = borrows_controller.parser()
parser.add_argument('patronId', type=str, help='Filter by patron ID', location='args', required=False)

@borrows_controller.route('/')
class BorrowList(borrows_controller.Resource):
    @borrows_controller.doc("Get all borrows")
    @borrows_controller.expect(parser)
    @borrows_controller.marshal_list_with(Borrow, code=200)
    def get(self):
        """Get all borrows with optional patron filtering"""
        patron_id = request.args.get('patronId')
        
        # Build query
        query = {}
        if patron_id:
            query["patron_id"] = patron_id
        
        # Get borrows and sort by statusLastUpdatedAt DESC
        borrows = list(borrows_collection.find(query).sort("statusLastUpdatedAt", -1))
        
        # Serialize and format response
        result = []
        for borrow in borrows:
            borrow_doc = serialize_mongo_doc(borrow)
            # Map fields for API response
            borrow_doc["patronId"] = borrow_doc.pop("patron_id", "")
            borrow_doc["copyId"] = borrow_doc.pop("copy_id", "") 
            result.append(borrow_doc)
        
        return result
    
    @borrows_controller.doc("Create a new borrow")
    @borrows_controller.expect(BorrowCreate)
    @borrows_controller.marshal_with(Borrow, code=201)
    def post(self):
        """Create a new borrow"""
        data = request.get_json()
        
        patron_id = data["patronId"]
        copy_id = data["copyId"]
        
        # Validate patron exists
        patron_object_id = str_to_objectid(patron_id)
        if not patron_object_id or not patrons_collection.find_one({"_id": patron_object_id}):
            abort(404, "Patron not found")
        
        # Validate copy exists
        copy_object_id = str_to_objectid(copy_id)
        if not copy_object_id or not copies_collection.find_one({"_id": copy_object_id}):
            abort(404, "Copy not found")
        
        # Check if copy is available
        if get_copy_status(copy_id) != "AVAILABLE":
            abort(400, "Copy is not available for borrowing")
        
        now = datetime.now()
        borrow_doc = {
            "patron_id": patron_id,
            "copy_id": copy_id,
            "status": "BORROWING",
            "createdAt": now,
            "statusLastUpdatedAt": now
        }
        
        result = borrows_collection.insert_one(borrow_doc)
        borrow_doc["_id"] = result.inserted_id
        
        # Format response
        borrow_response = serialize_mongo_doc(borrow_doc)
        borrow_response["patronId"] = borrow_response.pop("patron_id")
        borrow_response["copyId"] = borrow_response.pop("copy_id")
        
        return borrow_response, 201

@borrows_controller.route('/<string:borrow_id>')
class BorrowItem(borrows_controller.Resource):
    @borrows_controller.doc("Get borrow by ID")
    @borrows_controller.marshal_with(Borrow, code=200)
    def get(self, borrow_id):
        """Get a specific borrow by ID"""
        object_id = str_to_objectid(borrow_id)
        if not object_id:
            abort(404, "Invalid borrow ID")
        
        borrow = borrows_collection.find_one({"_id": object_id})
        if not borrow:
            abort(404, "Borrow not found")
        
        # Format response
        borrow_response = serialize_mongo_doc(borrow)
        borrow_response["patronId"] = borrow_response.pop("patron_id", "")
        borrow_response["copyId"] = borrow_response.pop("copy_id", "")
        
        return borrow_response
    
    @borrows_controller.doc("Update borrow status by ID")
    @borrows_controller.expect(BorrowUpdate)
    @borrows_controller.marshal_with(Borrow, code=200)
    def patch(self, borrow_id):
        """Update borrow status"""
        object_id = str_to_objectid(borrow_id)
        if not object_id:
            abort(404, "Invalid borrow ID")
        
        data = request.get_json()
        
        if "status" not in data:
            abort(400, "Status is required")
        
        valid_statuses = ["BORROWING", "RETURNED", "LOST"]
        if data["status"] not in valid_statuses:
            abort(400, f"Invalid status. Must be one of: {valid_statuses}")
        
        update_doc = {
            "status": data["status"],
            "statusLastUpdatedAt": datetime.now()
        }
        
        result = borrows_collection.find_one_and_update(
            {"_id": object_id},
            {"$set": update_doc},
            return_document=True
        )
        
        if not result:
            abort(404, "Borrow not found")
        
        # Format response
        borrow_response = serialize_mongo_doc(result)
        borrow_response["patronId"] = borrow_response.pop("patron_id", "")
        borrow_response["copyId"] = borrow_response.pop("copy_id", "")
        
        return borrow_response
    
    @borrows_controller.doc("Delete borrow by ID")
    def delete(self, borrow_id):
        """Delete a borrow"""
        object_id = str_to_objectid(borrow_id)
        if not object_id:
            abort(404, "Invalid borrow ID")
        
        result = borrows_collection.delete_one({"_id": object_id})
        
        if result.deleted_count == 0:
            abort(404, "Borrow not found")
        
        return "", 204