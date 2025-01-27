from django import template

register = template.Library()

@register.filter
def split(value, delimiter=':'):
    """
    Divide una cadena usando el delimitador especificado (por defecto ':').
    """
    return value.split(delimiter)
