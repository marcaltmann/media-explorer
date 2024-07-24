from django import template

register = template.Library()


@register.filter()
def timecode(value: int, format: str = "default") -> str:
    hours = int(value // 3600)
    minutes = int((value % 3600) // 60)
    seconds = int(value % 60)

    if format == "iso8601":
        return f"PT{hours:01}H{minutes:01}M{seconds:01}S"
    else:
        return f"{hours:01}:{minutes:02}:{seconds:02}"
