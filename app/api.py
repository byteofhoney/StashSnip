import re
from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, jsonify, request

from app.db import snippets_collection
from app.models import format_snippet

api = Blueprint("api", __name__)


@api.route("/snippets", methods=["GET"])
def get_snippets():
    """
    GET /api/snippets
    Optional query parameters: ?q=search_term&language=py&tag=flask
    Returns a list of snippet documents in JSON format.
    """
    query = request.args.get("q", "").strip()
    tag = request.args.get("tag", "").strip()
    language = request.args.get("language", "").strip()

    filters = {}
    if query:
        escaped_query = re.escape(query)
        filters["$or"] = [
            {"title": {"$regex": escaped_query, "$options": "i"}},
            {"description": {"$regex": escaped_query, "$options": "i"}},
        ]
    if tag:
        filters["tags"] = tag
    if language:
        filters["language"] = language

    snippets = list(snippets_collection.find(filters).sort("created_at", -1))
    formatted_snippets = [format_snippet(dict(s)) for s in snippets]
    return jsonify(formatted_snippets), 200


@api.route("/snippets/<id>", methods=["GET"])
def get_snippet(id):
    """
    GET /api/snippets/<id>
    Returns a single snippet document by ID or 404 if not found.
    """
    try:
        obj_id = ObjectId(id)
    except (InvalidId, TypeError):
        return jsonify({"error": "Snippet not found"}), 404

    snippet = snippets_collection.find_one({"_id": obj_id})
    if not snippet:
        return jsonify({"error": "Snippet not found"}), 404

    return jsonify(format_snippet(dict(snippet))), 200
