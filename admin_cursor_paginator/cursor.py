from base64 import b64decode, b64encode
from collections import namedtuple
from datetime import datetime


Cursor = namedtuple('Cursor', ['value', 'is_reverse', 'number'])

delimiter = '|||'


def encode_cursor(cursor):
    parts = [encode_value(x) for x in cursor]
    return b64encode(delimiter.join(parts).encode('utf8')).decode('ascii')


def decode_cursor(encoded_cursor):
    try:
        cursor_str = b64decode(encoded_cursor.encode('ascii')).decode('utf8')
        parts = cursor_str.split(delimiter)
        return Cursor(
            value=decode_value(parts[0]),
            is_reverse=bool(parts[1]),
            number=int(parts[2]),
        )
    except (TypeError, ValueError):
        return None


def encode_value(val):
    if not val:
        return ''
    # datetime.__str__ applies `isoformat()` under the hood
    # but we do this explicitly for the sake of clarity
    if isinstance(val, datetime):
        return val.isoformat()
    return str(val)


def decode_value(val):
    if not val:
        raise ValueError
    try:
        return _decode_datetime(val)
    except ValueError:
        return val


def _decode_datetime(val):
    try:
        return datetime.fromisoformat(val)
    except AttributeError:
        pass

    # back compat for python versions prior to 3.7
    # (they don't have `fromisoformat` method)
    from django.utils.dateparse import parse_datetime

    res = parse_datetime(val)
    if res:
        return res

    raise ValueError
