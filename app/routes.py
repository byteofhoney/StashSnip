from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from app.db import snippets_collection
from app.forms import SnippetForm
from app.models import make_snippet
from bson import ObjectId
from app.utils import parse_tags
from datetime import datetime
import json as _json

main = Blueprint("main", __name__)

@main.route("/")
def index():
    query = request.args.get("q", "")
    tag = request.args.get("tag", "")
    language = request.args.get("language", "")

    filters = {}

    if query:
        filters["$or"] = [
            {"title": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    if tag:
        filters["tags"] = tag
    if language:
        filters["language"] = language

    snippets = list(snippets_collection.find(filters).sort("created_at", -1))

    languages = snippets_collection.distinct("language")

    return render_template("index.html", 
        snippets=snippets, 
        query=query, 
        tag=tag,
        language=language,
        languages=languages
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
        tags=tags
    )
        snippets_collection.insert_one(snippet)
        flash("Snip saved successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("add.html", form=form)


@main.route("/export")
def export_snippets():
    snapshots = list(snippets_collection.find().sort("created_at", -1))
    payload = []
    for snip in snapshots:
        snip["_id"] = str(snip.get("_id"))
        payload.append({
            "title": snip.get("title"),
            "language": snip.get("language"),
            "code": snip.get("code"),
            "description": snip.get("description") or "",
            "tags": snip.get("tags") or [],
        })
    filename = f"stashsnip-export-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.json"
    return Response(
        _json.dumps(payload, ensure_ascii=False, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'},
    )

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
            {"$set": {
                "title": form.title.data,
                "language": form.language.data,
                "code": form.code.data,
                "description": form.description.data,
                "tags": tags,
                "updated_at": datetime.utcnow()
            }}
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
