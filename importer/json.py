import typing
from datetime import date, datetime
from decimal import Decimal
from json import JSONEncoder, dumps

from django.db.models import Model
from language_tags.Tag import Tag


def as_json(payload: typing.Any) -> typing.Text:
    """
    Converts a value into a JSON string representation.
    """
    return dumps(payload, cls=CustomJsonEncoder)


class CustomJsonEncoder(JSONEncoder):
    """
    Extends the default JSON encoder with support for additional types.
    """

    def default(self, o: typing.Any) -> typing.Any:
        if isinstance(o, (date, datetime)):
            return o.isoformat()

        if isinstance(o, (Decimal, Model, Tag)):
            return str(o)

        return super().default(o)
