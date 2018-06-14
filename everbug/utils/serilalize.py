from functools import singledispatch

from django.core.serializers import serialize
from django.db.models import Model, QuerySet
from django.forms import Form
from django.forms.models import model_to_dict


@singledispatch
def serial(obj):
    """ JSON Encoder
    Returns (for all nested elements of lists and dicts):
        * int, float, str, bool - as is
        * tuple, set and frozenset - as list
        * django form and model - as dict
        * django queryset via builtin django serializer
        * others - as str
    """
    if isinstance(obj, (int, float, str, bool)):
        return obj
    return str(obj)


@serial.register(dict)
def _(obj):
    return {k: serial(v) for k, v in obj.items()}


@serial.register(set)
@serial.register(list)
@serial.register(tuple)
@serial.register(frozenset)
def _(obj):
    return [serial(i) for i in obj]


@serial.register(Form)
def _(obj):
    fields = obj.fields
    return {f: type(fields[f]).__name__ for f in fields}


@serial.register(QuerySet)
def _(obj):
    return serialize('python', obj)


@serial.register(Model)
def _(obj):
    return model_to_dict(obj)
