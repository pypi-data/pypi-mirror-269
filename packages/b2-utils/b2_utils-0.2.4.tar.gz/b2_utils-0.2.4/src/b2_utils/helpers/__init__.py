import importlib as _importlib
import locale as _locale
import random as _random
import urllib.parse as _urlparse
from typing import Any
from urllib.parse import urlencode as _urlencode

from b2_utils.helpers.auth import *  # noqa

__all__ = [
    "random_hex_color",
    "get_nested_attr",
    "update_url_querystring",
    "days_to_seconds",
    "cpf_parser",
    "cnpj_parser",
    "currency_parser",
]


def days_to_seconds(days):
    return days * 24 * 60 * 60


def random_hex_color(min_color=0x000000, max_color=0xFFFFFF) -> str:
    """Returns a random hexadecimal color in range [min_color, max_color], including
    both end points.

    Parameters
    ---------
    min_color : int
        Minimum value for color (default 0x000000)
    max_color : int
        Maximum value for color (default 0xFFFFFF)

    Returns
    -------
    str
        A random color "#XXXXXX" that is between min_color and max_color values.
    """

    return "#%06x".upper() % _random.randint(min_color, max_color)  # noqa: S311


def get_nested_attr(obj: any, path: str, raise_exception=False, default=None):
    """Gets nested object attributes, raising exceptions only when specified.

    Parameters
    ---------
    obj : any
        The object which attributes will be obtained
    path : str
        Attribute path separated with dots ('.') as usual
    raise_exception : bool = False
        If this value sets to True, an exception will be raised if an attribute cannot
        be obtained, even if default value is specified
    default : any = None
        A default value that's returned if the attribute can't be obtained. This
        parameter is ignored if raise_exception=True

    Returns
    -------
    any
        Attribute value or default value specified if any error occours while trying
        to get object attribute
    """

    for path_attr in path.split("."):
        if raise_exception:
            obj = getattr(obj, path_attr)
        else:
            obj = getattr(obj, path_attr, default)

    return obj


def update_url_querystring(
    url: str,
    params: dict,
    aditional_params: list[str] | None = None,
) -> str:
    """Updates the queryparams given a URL.

    Parameters
    ---------
    url: str
        The url you want to update.
    params: dict
        A dict with the new queryparams values.

    Returns
    -------
    str
        The full url, with updated queryparams.
    """
    url_parts = list(_urlparse.urlparse(url))
    query = dict(_urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = _urlencode(query)
    if aditional_params:
        params = "&".join(aditional_params)
        if url_parts[4]:
            url_parts[4] += f"&{params}"

        else:
            url_parts[4] = params

    return _urlparse.urlunparse(url_parts)


def cpf_parser(value: str) -> str:
    return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:12]}"


def cnpj_parser(value: str) -> str:
    return f"{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}"


def currency_parser(value: str | int, encoding: str = "pt_BR.UTF-8") -> str:
    _locale.setlocale(_locale.LC_ALL, encoding)

    return _locale.currency(int(value) / 100, grouping=True)


def get_component(
    path: str,
    raise_exception: bool = True,
    default: Any | None = None,
) -> Any:
    """Retrieve a component from a specified Python module by its dotted path.

    This function imports a Python module and retrieves a component within it using the provided path. The path
    should be in the form 'module_name.component_name'. If the component is not found, and 'raise_exception' is
    set to True, a `AttributeError` will be raised. If 'raise_exception' is set to False, the 'default' value
    will be returned if the component is not found.

    Args:
        path (str): The dotted path to the desired component, e.g., 'module_name.component_name'.
        raise_exception (bool, optional): Whether to raise an exception if the component is not found.
            Defaults to True.
        default (any, optional): The default value to return if the component is not found when 'raise_exception'
            is set to False. Defaults to None.

    Returns:
        any: The requested component if found, or the default value if 'raise_exception' is set to False.

    Raises:
        AttributeError: If 'raise_exception' is True and the component is not found.

    Example:
        get_component("my_module.my_function")  # Returns the 'my_function' from 'my_module'.

    """
    module_name, component_name = path.rsplit(".", 1)
    module = _importlib.import_module(module_name)
    if raise_exception:
        return getattr(module, component_name)

    return getattr(module, component_name, default)


class Alias:
    def __init__(self, source_name, transform=None):
        self.source_name = source_name
        self.transform = transform

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        value = getattr(obj, self.source_name)

        if self.transform:
            value = self.transform(value)

        return value

    def __set__(self, obj, value):
        if self.transform:
            value = self.transform(value)

        setattr(obj, self.source_name, value)
