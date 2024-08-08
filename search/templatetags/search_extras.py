from collections.abc import Iterable

from django import template

register = template.Library()


@register.simple_tag(name="dynamic_qs", takes_context=True)
def dynamic_qs(context, *args):
    """
    Like Django's built-in querystring tag, but accepts dynamic keys.
    """
    query_dict = context.request.GET
    query_dict = query_dict.copy()

    kwargs = dict()
    it = iter(args)
    for value in it:
        count = next(it)
        kwargs[value] = count

    for key, value in kwargs.items():
        if value is None:
            if key in query_dict:
                del query_dict[key]
        elif isinstance(value, Iterable) and not isinstance(value, str):
            query_dict.setlist(key, value)
        else:
            query_dict[key] = value
    if not query_dict:
        return ""
    query_string = query_dict.urlencode()
    return f"?{query_string}"
