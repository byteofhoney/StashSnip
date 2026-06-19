from datetime import datetime

def make_snippet(title, language, code, description, tags):
    """
    Returns a clean snippet document ready to insert into MongoDB.
    Centralizing this means if we ever change the schema,
    we change it in one place only.
    """
    return {
        "title": title,
        "language": language,
        "code": code,
        "description": description,
        "tags": tags,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

def format_snippet(snippet):
    """
    Converts ObjectId to string so we can safely pass
    snippets around without MongoDB-specific types.
    """
    snippet["_id"] = str(snippet["_id"])
    return snippet