from flask import Blueprint, render_template
from app.db import snippets_collection

main = Blueprint("main", __name__)

@main.route("/")
def index():
    snippets = list(snippets_collection.find().sort("created_at", -1))
    return render_template("index.html", snippets=snippets)