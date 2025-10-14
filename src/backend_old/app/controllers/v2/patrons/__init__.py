from ...common import Controller
from .dto.patron import patron_dto, patron_create_dto, patron_update_dto
from flask import request, jsonify
from flask_restx import abort
from datetime import datetime
from ...db import patrons_collection, serialize_mongo_doc, str_to_objectid

patrons_controller = Controller("patrons", __name__, enable_hateoas=True)

Patron = patron_dto(patrons_controller)
PatronCreate = patron_create_dto(patrons_controller)
PatronUpdate = patron_update_dto(patrons_controller)

@patrons_controller.route('/')
class PatronList(patrons_controller.Resource):
    @patrons_controller.doc("Get all patrons")
    @patrons_controller.marshal_list_with(Patron, code=200)
    def get(self):
        """Get all patrons with pagination"""
        patrons = list(patrons_collection.find())
        return [serialize_mongo_doc(patron) for patron in patrons]
    
    @patrons_controller.doc("Create a new patron")
    @patrons_controller.expect(PatronCreate)
    @patrons_controller.marshal_with(Patron, code=201)
    def post(self):
        """Create a new patron"""
        data = request.get_json()
        
        patron_doc = {
            "name": data["name"]
        }
        
        result = patrons_collection.insert_one(patron_doc)
        patron_doc["_id"] = result.inserted_id
        
        return serialize_mongo_doc(patron_doc), 201

@patrons_controller.route('/<string:patronId>')
class PatronItem(patrons_controller.Resource):
    @patrons_controller.doc("Get patron by ID")
    @patrons_controller.marshal_with(Patron, code=200)
    def get(self, patronId):
        """Get a specific patron by ID"""
        object_id = str_to_objectid(patronId)
        if not object_id:
            abort(404, "Invalid patron ID")
        
        patron = patrons_collection.find_one({"_id": object_id})
        if not patron:
            abort(404, "Patron not found")
        
        return serialize_mongo_doc(patron)
    
    @patrons_controller.doc("Update patron by ID")
    @patrons_controller.expect(PatronUpdate)
    @patrons_controller.marshal_with(Patron, code=200)
    def patch(self, patronId):
        """Update a patron"""
        object_id = str_to_objectid(patronId)
        if not object_id:
            abort(404, "Invalid patron ID")
        
        data = request.get_json()
        update_doc = {}
        
        if "name" in data:
            update_doc["name"] = data["name"]
        
        if not update_doc:
            abort(400, "No valid fields to update")
        
        result = patrons_collection.find_one_and_update(
            {"_id": object_id},
            {"$set": update_doc},
            return_document=True
        )
        
        if not result:
            abort(404, "Patron not found")
        
        return serialize_mongo_doc(result)
    
    @patrons_controller.doc("Delete patron by ID")
    def delete(self, patronId):
        """Delete a patron"""
        object_id = str_to_objectid(patronId)
        if not object_id:
            abort(404, "Invalid patron ID")
        
        result = patrons_collection.delete_one({"_id": object_id})
        
        if result.deleted_count == 0:
            abort(404, "Patron not found")
        
        return "", 204
