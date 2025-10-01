from ..common import Controller
from .dto.title import title_dto, title_create_dto, title_update_dto
from .dto.copy import copy_dto, copy_create_dto, copy_update_dto
from flask import request, jsonify
from flask_restx import abort
from datetime import datetime
from ..db import (titles_collection, copies_collection, borrows_collection, 
                  serialize_mongo_doc, str_to_objectid, get_copy_status, get_title_with_stats)

titles_controller = Controller("titles", __name__)

Title = title_dto(titles_controller)
TitleCreate = title_create_dto(titles_controller)
TitleUpdate = title_update_dto(titles_controller)
Copy = copy_dto(titles_controller)
CopyCreate = copy_create_dto(titles_controller)
CopyUpdate = copy_update_dto(titles_controller)

@titles_controller.route('/')
class TitleList(titles_controller.Resource):
    @titles_controller.doc("Get all titles")
    @titles_controller.marshal_list_with(Title, code=200)
    def get(self):
        """Get all titles with pagination"""
        titles = list(titles_collection.find())
        return [get_title_with_stats(title) for title in titles]
    
    @titles_controller.doc("Create a new title")
    @titles_controller.expect(TitleCreate)
    @titles_controller.marshal_with(Title, code=201)
    def post(self):
        """Create a new title"""
        data = request.get_json()
        
        title_doc = {
            "name": data["name"],
            "edition": data["edition"],
            "authors": data["authors"],
            "yearOfPublication": data["yearOfPublication"],
            "tags": data["tags"]
        }
        
        result = titles_collection.insert_one(title_doc)
        title_doc["_id"] = result.inserted_id
        
        return get_title_with_stats(title_doc), 201

@titles_controller.route('/<string:title_id>')
class TitleItem(titles_controller.Resource):
    @titles_controller.doc("Get title by ID")
    @titles_controller.marshal_with(Title, code=200)
    def get(self, title_id):
        """Get a specific title by ID"""
        object_id = str_to_objectid(title_id)
        if not object_id:
            abort(404, "Invalid title ID")
        
        title = titles_collection.find_one({"_id": object_id})
        if not title:
            abort(404, "Title not found")
        
        return get_title_with_stats(title)
    
    @titles_controller.doc("Update title by ID")
    @titles_controller.expect(TitleUpdate)
    @titles_controller.marshal_with(Title, code=200)
    def patch(self, title_id):
        """Update a title"""
        object_id = str_to_objectid(title_id)
        if not object_id:
            abort(404, "Invalid title ID")
        
        data = request.get_json()
        update_doc = {}
        
        for field in ["name", "edition", "authors", "yearOfPublication", "tags"]:
            if field in data:
                update_doc[field] = data[field]
        
        if not update_doc:
            abort(400, "No valid fields to update")
        
        result = titles_collection.find_one_and_update(
            {"_id": object_id},
            {"$set": update_doc},
            return_document=True
        )
        
        if not result:
            abort(404, "Title not found")
        
        return get_title_with_stats(result)
    
    @titles_controller.doc("Delete title by ID")
    def delete(self, title_id):
        """Delete a title and all its copies"""
        object_id = str_to_objectid(title_id)
        if not object_id:
            abort(404, "Invalid title ID")
        
        # Delete all copies of this title first
        copies_collection.delete_many({"title_id": title_id})
        
        # Delete the title
        result = titles_collection.delete_one({"_id": object_id})
        
        if result.deleted_count == 0:
            abort(404, "Title not found")
        
        return "", 204

@titles_controller.route('/<string:title_id>/copies')
class CopyList(titles_controller.Resource):
    @titles_controller.doc("Get all copies of a title")
    @titles_controller.marshal_list_with(Copy, code=200)
    def get(self, title_id):
        """Get all copies of a specific title"""
        object_id = str_to_objectid(title_id)
        if not object_id:
            abort(404, "Invalid title ID")
        
        # Check if title exists
        title = titles_collection.find_one({"_id": object_id})
        if not title:
            abort(404, "Title not found")
        
        # Get all copies for this title
        copies = list(copies_collection.find({"title_id": title_id}))
        
        title_copies = []
        for copy in copies:
            copy_doc = serialize_mongo_doc(copy)
            copy_doc["status"] = get_copy_status(copy_doc["id"])
            title_copies.append(copy_doc)
        
        return title_copies
    
    @titles_controller.doc("Create a new copy of a title")
    @titles_controller.expect(CopyCreate)
    @titles_controller.marshal_with(Copy, code=201)
    def post(self, title_id):
        """Create a new copy of a title"""
        object_id = str_to_objectid(title_id)
        if not object_id:
            abort(404, "Invalid title ID")
        
        # Check if title exists
        title = titles_collection.find_one({"_id": object_id})
        if not title:
            abort(404, "Title not found")
        
        data = request.get_json()
        
        copy_doc = {
            "title_id": title_id,
            "code": data["code"]
        }
        
        result = copies_collection.insert_one(copy_doc)
        copy_doc["_id"] = result.inserted_id
        
        copy_response = serialize_mongo_doc(copy_doc)
        copy_response["titleId"] = title_id
        copy_response["status"] = "AVAILABLE"
        
        return copy_response, 201

@titles_controller.route('/<string:title_id>/copies/<string:copy_id>')
class CopyItem(titles_controller.Resource):
    @titles_controller.doc("Get copy by ID")
    @titles_controller.marshal_with(Copy, code=200)
    def get(self, title_id, copy_id):
        """Get a specific copy by ID"""
        # Validate title exists
        title_object_id = str_to_objectid(title_id)
        if not title_object_id or not titles_collection.find_one({"_id": title_object_id}):
            abort(404, "Title not found")
        
        # Validate copy exists and belongs to title
        copy_object_id = str_to_objectid(copy_id)
        if not copy_object_id:
            abort(404, "Invalid copy ID")
        
        copy = copies_collection.find_one({"_id": copy_object_id, "title_id": title_id})
        if not copy:
            abort(404, "Copy not found or does not belong to this title")
        
        copy_response = serialize_mongo_doc(copy)
        copy_response["titleId"] = title_id
        copy_response["status"] = get_copy_status(copy_id)
        return copy_response
    
    @titles_controller.doc("Update copy by ID")
    @titles_controller.expect(CopyUpdate)
    @titles_controller.marshal_with(Copy, code=200)
    def patch(self, title_id, copy_id):
        """Update a copy"""
        # Validate title exists
        title_object_id = str_to_objectid(title_id)
        if not title_object_id or not titles_collection.find_one({"_id": title_object_id}):
            abort(404, "Title not found")
        
        # Validate copy exists and belongs to title
        copy_object_id = str_to_objectid(copy_id)
        if not copy_object_id:
            abort(404, "Invalid copy ID")
        
        data = request.get_json()
        update_doc = {}
        
        if "code" in data:
            update_doc["code"] = data["code"]
        
        if not update_doc:
            abort(400, "No valid fields to update")
        
        result = copies_collection.find_one_and_update(
            {"_id": copy_object_id, "title_id": title_id},
            {"$set": update_doc},
            return_document=True
        )
        
        if not result:
            abort(404, "Copy not found or does not belong to this title")
        
        copy_response = serialize_mongo_doc(result)
        copy_response["titleId"] = title_id
        copy_response["status"] = get_copy_status(copy_id)
        return copy_response
    
    @titles_controller.doc("Delete copy by ID")
    def delete(self, title_id, copy_id):
        """Delete a copy"""
        # Validate title exists
        title_object_id = str_to_objectid(title_id)
        if not title_object_id or not titles_collection.find_one({"_id": title_object_id}):
            abort(404, "Title not found")
        
        # Delete copy
        copy_object_id = str_to_objectid(copy_id)
        if not copy_object_id:
            abort(404, "Invalid copy ID")
        
        result = copies_collection.delete_one({"_id": copy_object_id, "title_id": title_id})
        
        if result.deleted_count == 0:
            abort(404, "Copy not found or does not belong to this title")
        
        return "", 204
