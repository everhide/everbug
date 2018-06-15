from django.db.models import Model, QuerySet
from django.forms import Form
from django.views import View


TYPE_DJANGO = (QuerySet, Form, Model)

TYPE_BUILTINS = (
    int,
    float,
    complex,
    bool,
    bytes,
    bytearray,
    str,
    tuple,
    set,
    frozenset,
    list,
    dict
)


class Ext:
    SIMPLE, ITERABLE, DJANGO, CLASS = 0, 1, 2, 3


def wrap_context(context):
    """ Wraps a django context dict into list of tuples
    :param context: django context dict
    :return: (list)
    """

    def wrap(key, val):
        """ Wraps a context element in a tuple.
        Result tuple contains:
            * name - name of context element
            * value - value of context element
            * class - repr class name of a value
            * ext - flag of type group for extension
            * count - length of value if it's possible or makes sense
        :param key: name of context element.
        :param val: value of context element.
        :return: (tuple)
        """

        cls, ext, count = val.__class__.__name__, Ext.CLASS, 0
        if isinstance(val, TYPE_BUILTINS):
            if not hasattr(val, '__len__') and not hasattr(val, '__iter__'):
                ext = Ext.SIMPLE
            else:
                ext, count = Ext.ITERABLE, len(val)
        elif isinstance(val, TYPE_DJANGO):
            ext = Ext.DJANGO
            if isinstance(val, QuerySet):
                count = len(val)
                cls = 'QuerySet: %s' % val.model.__name__
            elif isinstance(val, Model):
                cls, count = 'Model: %s' % val.__class__.__name__, 1
            elif isinstance(val, Form):
                cls, count = 'Form: %s' % val.__class__.__name__, 1
        else:
            if hasattr(val, '__name__'):
                cls = 'Class: %s' % val.__name__
            else:
                cls = 'Instance: %s' % val.__class__.__name__
            # for ugly representation other classes and instances
            val = val if len(str(val)) < 50 else '%s...' % str(val)[:50]

        return key, val, cls, ext, count

    items = [wrap(k, v) for k, v in context.items() if not isinstance(v, View)]
    return sorted(items, key=lambda item: item[3])
