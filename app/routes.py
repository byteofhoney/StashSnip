from datetime import datetime, UTC
from math import ceil
import json

from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from app.db import snippets_collection
from app.forms import SnippetForm
from app.models import make_snippet
from app.utils import parse_tags

main = Blueprint("main", __name__)
PAGE_SIZE = 12


@main.route("/")
def index():
    query = request.args.get("q", "")
    tag = request.args.get("tag", "")
    language = request.args.get("language", "")
    page = request.args.get("page", 1, type=int)
    page = max(page, 1)

    filters = {}

    if query:
        filters["$or"] = [
            {"title": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}},
        ]
    if tag:
        filters["tags"] = tag
    if language:
        filters["language"] = language

    total_snippets = snippets_collection.count_documents(filters)
    total_pages = ceil(total_snippets / PAGE_SIZE) if total_snippets else 0

    if total_pages and page > total_pages:
        page = total_pages

    snippets = list(
        snippets_collection.find(filters)
        .sort("created_at", -1)
        .skip((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
    )

    languages = snippets_collection.distinct("language")
    pagination_params = {
        key: value
        for key, value in {
            "q": query,
            "tag": tag,
            "language": language,
        }.items()
        if value
    }

    return render_template(
        "index.html",
        snippets=snippets,
        total_snippets=total_snippets,
        query=query,
        tag=tag,
        language=language,
        languages=languages,
        page=page,
        total_pages=total_pages,
        pagination_params=pagination_params,
    )


@main.route("/add", methods=["GET", "POST"])
def add_snippet():
    form = SnippetForm()
    if form.validate_on_submit():
        tags = parse_tags(form.tags.data)
        snippet = make_snippet(
            title=form.title.data,
            language=form.language.data,
            code=form.code.data,
            description=form.description.data,
            tags=tags,
        )
        snippets_collection.insert_one(snippet)
        flash("Snip saved successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("add.html", form=form)


@main.route("/snippet/<id>")
def view_snippet(id):
    snippet = snippets_collection.find_one({"_id": ObjectId(id)})
    if not snippet:
        return render_template("404.html"), 404
    return render_template("snippet.html", snippet=snippet)

@main.route("/delete/<id>", methods=["POST"])
def delete_snippet(id):
    snippets_collection.delete_one({"_id": ObjectId(id)})
    flash("Snip deleted.", "success")
    return redirect(url_for("main.index"))

@main.route("/edit/<id>", methods=["GET", "POST"])
def edit_snippet(id):
    snippet = snippets_collection.find_one({"_id": ObjectId(id)})
    if not snippet:
        return render_template("404.html"), 404

    form = SnippetForm()

    if form.validate_on_submit():
        tags = parse_tags(form.tags.data)
        snippets_collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "title": form.title.data,
                    "language": form.language.data,
                    "code": form.code.data,
                    "description": form.description.data,
                    "tags": tags,
                    "updated_at": datetime.now(UTC),
                }
            },
        )
        flash("Snip updated!", "success")
        return redirect(url_for("main.view_snippet", id=id))

    # Pre-fill form with existing data
    form.title.data = snippet["title"]
    form.language.data = snippet["language"]
    form.code.data = snippet["code"]
    form.description.data = snippet.get("description", "")
    form.tags.data = ", ".join(snippet.get("tags", []))

    return render_template("edit.html", form=form, snippet=snippet)


@main.route("/export")
def export_snippets():
    """Export all snippets as downloadable JSON file"""
    # Get all snippets from database
    snippets = list(snippets_collection.find())
    
    # Convert ObjectId to string for JSON compatibility
    for snippet in snippets:
        snippet["_id"] = str(snippet["_id"])
        # Convert datetime objects to ISO format strings
        if "created_at" in snippet:
            snippet["created_at"] = snippet["created_at"].isoformat()
        if "updated_at" in snippet:
            snippet["updated_at"] = snippet["updated_at"].isoformat()
    
    # Return JSON with download headers
    return jsonify(snippets), 200, {
        "Content-Disposition": "attachment; filename=stash_snip_backup.json",
        "Content-Type": "application/json"
    }
