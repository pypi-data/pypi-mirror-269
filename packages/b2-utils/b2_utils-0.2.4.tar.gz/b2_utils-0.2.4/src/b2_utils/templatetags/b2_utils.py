from django import template as _template
from django.conf import settings as _settings

from b2_utils import helpers as _helpers

__all__ = [
    "get_settings",
    "cents_to_brl",
    "cnpj_parse",
    "cpf_parse",
    "index",
    "classname",
    "word",
    "get",
]

register = _template.Library()


@register.simple_tag(name="settings")
def get_settings(name):
    return getattr(_settings, name, "")


@register.filter(name="brl")
def cents_to_brl(value: str | int):
    return _helpers.currency_parser(value)


@register.filter(name="cnpj")
def cnpj_parse(value: str) -> str:
    return _helpers.cnpj_parser(value)


@register.filter(name="cpf")
def cpf_parse(cpf_number: str) -> str:
    return _helpers.cpf_parser(cpf_number)


@register.filter
def index(my_list, idx):
    try:
        return my_list[idx]
    except (IndexError, TypeError):
        return None


@register.filter
def classname(obj):
    return obj.__class__.__name__


@register.filter
def word(text: str, index: int):
    if text:
        return text.split()[index]

    return None


@register.filter
def get(dictionary: dict, key: str):
    if isinstance(dictionary, dict):
        return dictionary.get(key)

    return dictionary
