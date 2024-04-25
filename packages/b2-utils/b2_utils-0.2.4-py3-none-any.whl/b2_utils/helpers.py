import re as _re
from datetime import datetime as _datetime
from io import BytesIO as _BytesIO
from zoneinfo import ZoneInfo as _ZoneInfo

import requests as _requests
from django.conf import settings as _settings

from b2_utils.typing import RangeHeader as _RangeHeader

__all__ = [
    "pascal_to_snake",
    "string_to_date_obj",
    "load_from_url",
]


def pascal_to_snake(name):
    return _re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def string_to_date_obj(date: str, format: str):
    tz_info = _ZoneInfo(_settings.TIME_ZONE)
    date = date.replace("Z", "")

    return _datetime.strptime(date, format).astimezone(tz_info).date()


def load_from_url(url: str):
    """
    This function is used to load a file from a url and return a buffer.
    """
    buffer = _BytesIO()
    write_in_buffer(url, buffer)

    buffer.seek(0)

    return buffer


def get_range_header(
    buffer: _BytesIO,
    content_length: int,
) -> (bool, _RangeHeader | None):
    """
    This function is used to get the range header from a buffer.
    """
    buffer_size = buffer.__sizeof__()
    writer_all_content = buffer_size >= content_length

    if not writer_all_content:
        return writer_all_content, {"Range": f"bytes={buffer_size}-{content_length}"}

    return writer_all_content, None


def write_in_buffer(
    url: str,
    buffer: _BytesIO,
    headers: _RangeHeader | None = None,
    chunk_size: int = 1024 * 1024,
):
    """
    This function is used to write in a buffer from a url.
    """
    response = _requests.get(
        url,
        stream=True,
        headers=headers,
        timeout=10,
    )
    if response.ok:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                buffer.write(chunk)

        is_complete, header = get_range_header(
            buffer,
            int(response.headers["Content-Length"]),
        )

        if not is_complete:
            write_in_buffer(url, buffer, header)

    return buffer
