from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import snippets_collection
from app.forms import SnippetForm
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/")
def index():
    snippets = list(snippets_collection.find().sort("created_at", -1))
    return render_template("index.html", snippets=snippets)

@main.route("/add", methods=["GET", "POST"])
def add_snippet():
    form = SnippetForm()
    if form.validate_on_submit():
        tags = [tag.strip() for tag in form.tags.data.split(",") if tag.strip()]
        snippet = {
            "title": form.title.data,
            "language": form.language.data,
            "code": form.code.data,
            "description": form.description.data,
            "tags": tags,
            "created_at": datetime.utcnow()
        }
        snippets_collection.insert_one(snippet)
        flash("Snip saved successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("add.html", form=form)