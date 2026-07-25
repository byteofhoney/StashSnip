from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
@main.route('/import', methods=['GET','POST'])
def import_snippets():
    if request.method == 'POST':
        uploaded = request.files.get('json_file')
        if not uploaded or uploaded.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('main.import_snippets'))
        if not uploaded.filename.lower().endswith('.json'):
            flash('Please upload a .json file.', 'error')
            return redirect(url_for('main.import_snippets'))
        try:
            payload = _json.loads(uploaded.read().decode('utf-8'))
        except Exception as exc:
            flash(f'Invalid JSON file: {exc}', 'error')
            return redirect(url_for('main.import_snippets'))

        items = payload if isinstance(payload, list) else payload.get('snippets') or []
        if not isinstance(items, list) or not items:
            flash('JSON must be an array of snippet objects.', 'error')
            return redirect(url_for('main.import_snippets'))

        docs=[]
        for item in items:
            if not isinstance(item, dict):
                continue
            title=str(item.get('title') or '').strip()
            language=str(item.get('language') or 'other').strip()
            code=str(item.get('code') or '').strip()
            description=str(item.get('description') or '').strip()
            tags=item.get('tags') or []
            if not isinstance(tags, list):
                tags=[str(tags)]
            tags=[str(t).strip() for t in tags if str(t).strip()]
            if not title or not code:
                continue
            docs.append(make_snippet(title=title, language=language, code=code, description=description, tags=tags))
        if not docs:
            flash('No valid snippets found in file.', 'error')
            return redirect(url_for('main.import_snippets'))

        snippets_collection.insert_many(docs)
        flash(f'Imported {len(docs)} snippet(s).', 'success')
        return redirect(url_for('main.index'))
    return render_template('import.html')
