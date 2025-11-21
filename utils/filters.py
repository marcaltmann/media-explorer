"""Filters for Jinja2 templates."""

def duration_format(value: float) -> str:
    """Format media duration."""
    hours = int(value // 3600)
    minutes = int((value % 3600) // 60)
    secs = int(value % 60)
    if hours > 0:
        return f"{hours}h{minutes}m{secs}s"
    else:
        return f"{minutes}m{secs}s"
