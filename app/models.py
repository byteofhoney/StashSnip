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
    Converts ObjectId and datetime objects so we can safely pass
    snippets around or return them as JSON without serialization errors.
    """
    snippet["_id"] = str(snippet["_id"])
    if isinstance(snippet.get("created_at"), datetime):
        snippet["created_at"] = snippet["created_at"].isoformat()
    if isinstance(snippet.get("updated_at"), datetime):
        snippet["updated_at"] = snippet["updated_at"].isoformat()
    return snippet