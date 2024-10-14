from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    elif hasattr(dictionary, '_dict_items'):
        return dict(dictionary).get(key)
    return None
