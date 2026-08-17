from datetime import datetime, UTC

def make_snippet(title, language, code, description, tags):
    return {
        "title": title,
        "language": language,
        "code": code,
        "description": description,
        "tags": tags,
        "deleted": False,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    }

def format_snippet(snippet):
    """
    Converts ObjectId to string so we can safely pass
    snippets around without MongoDB-specific types.
    """
    snippet["_id"] = str(snippet["_id"])
    return snippet