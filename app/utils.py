def parse_tags(tags_string):
    """
    Converts a comma separated string of tags into a clean list.
    e.g. " python, flask , mongodb " -> ["python", "flask", "mongodb"]
    """
    if not tags_string:
        return []
    return [tag.strip().lower() for tag in tags_string.split(",") if tag.strip()]