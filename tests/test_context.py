from unittest import TestCase
from unittest.mock import Mock

from everbug.utils.context import Ext, wrap_context

from tests.stub.forms import TestForm
from tests.stub.models import Entity as TestModel


class TestBuiltins(TestCase):

    def test_instance(self):
        i = Mock()
        ref = ('i', i, 'Instance: %s' % i.__class__.__name__, Ext.CLASS, 0)
        self.assertEqual(wrap_context({'i': i}), [ref])

    def test_class(self):
        ref = ('cls', Mock, 'Class: %s' % Mock.__name__, Ext.CLASS, 0)
        self.assertEqual(wrap_context({'cls': Mock}), [ref])

    def test_int(self):
        ref = ('int', 1, 'int', Ext.SIMPLE, 0)
        self.assertEqual(wrap_context({'int': 1}), [ref])

    def test_float(self):
        ref = ('float', 0.1, 'float', Ext.SIMPLE, 0)
        self.assertEqual(wrap_context({'float': 0.1}), [ref])

    def test_complex(self):
        ref = ('complex', 1 + 1j, 'complex', Ext.SIMPLE, 0)
        self.assertEqual(wrap_context({'complex': 1 + 1j}), [ref])

    def test_bool(self):
        ref = ('bool', True, 'bool', Ext.SIMPLE, 0)
        self.assertEqual(wrap_context({'bool': True}), [ref])

    def test_bytes(self):
        ref = ('bytes', b'\x00', 'bytes', Ext.ITERABLE, 1)
        self.assertEqual(wrap_context({'bytes': bytes([0])}), [ref])

    def test_bytearray(self):
        ref = ('bytearray', b'\x00\x01', 'bytearray', Ext.ITERABLE, 2)
        self.assertEqual(wrap_context({'bytearray': bytearray([0, 1])}), [ref])

    def test_str(self):
        ref = ('str', 'foo', 'str', Ext.ITERABLE, 3)
        self.assertEqual(wrap_context({'str': 'foo'}), [ref])

    def test_tuple(self):
        ref = ('tuple', (0, 1), 'tuple', Ext.ITERABLE, 2)
        self.assertEqual(wrap_context({'tuple': (0, 1)}), [ref])

    def test_list(self):
        ref = ('list', [0, 1], 'list', Ext.ITERABLE, 2)
        self.assertEqual(wrap_context({'list': [0, 1]}), [ref])

    def test_dict(self):
        ref = ('dict', {'var': None}, 'dict', Ext.ITERABLE, 1)
        self.assertEqual(wrap_context({'dict': {'var': None}}), [ref])

    def test_set(self):
        ref = ('set', {0, 1}, 'set', Ext.ITERABLE, 2)
        self.assertEqual(wrap_context({'set': {0, 1}}), [ref])

    def test_frozenset(self):
        ref = ('frozenset', frozenset([0, 1]), 'frozenset', Ext.ITERABLE, 2)
        self.assertEqual(wrap_context({'frozenset': frozenset([0, 1])}), [ref])

    def test_form(self):
        form = TestForm()
        ref = ('form', form, 'Form: %s' % TestForm.__name__, Ext.DJANGO, 1)
        self.assertEqual(wrap_context({'form': form}), [ref])

    def test_model(self):
        model = TestModel.objects.first()
        ref = ('model', model, 'Model: %s' % TestModel.__name__, Ext.DJANGO, 1)
        self.assertEqual(wrap_context({'model': model}), [ref])

    def test_queryset(self):
        qs = TestModel.objects.all()[:2]
        ref = ('qs', qs, 'QuerySet: %s' % TestModel.__name__, Ext.DJANGO, 2)
        self.assertEqual(wrap_context({'qs': qs}), [ref])
