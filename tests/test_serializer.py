from unittest import TestCase
from unittest.mock import Mock

from django.core.serializers import serialize
from django.forms.models import model_to_dict

from everbug.utils.serilalize import serial

from tests.stub.forms import TestForm
from tests.stub.models import Entity


class TestSerial(TestCase):

    def test_as_is_int_float_bool_str(self):
        for item in (1, 0.1, True, 'string'):
            self.assertEqual(item, serial(item))

    def test_iterables(self):
        for item in (frozenset([0]), {0}, (0,)):
            self.assertEqual([0], serial(item))

    def test_dict(self):
        sample_dict = {'key': 'value'}
        self.assertEqual(sample_dict, serial(sample_dict))

    def test_dict_nested(self):
        pattern = {'key': {'sub_key': [0, 1, 2]}}
        test_dict = {'key': {'sub_key': frozenset([0, 1, 2])}}
        self.assertEqual(pattern, serial(test_dict))

    def test_list(self):
        sample_list = [0, 1, 2]
        self.assertEqual(sample_list, serial(sample_list))

    def test_list_nested(self):
        pattern = [0, [1, [2, [3]]]]
        test_list = [0, (1, (2, frozenset({3})))]
        self.assertEqual(pattern, serial(test_list))

    def test_form(self):
        form = TestForm()
        fields = form.fields
        pattern = {f: type(fields[f]).__name__ for f in fields}
        self.assertEqual(pattern, serial(form))

    def test_queryset(self):
        items = Entity.objects.all()
        pattern = serialize('python', items)
        self.assertEqual(pattern, serial(items))

    def test_model(self):
        item = Entity.objects.first()
        pattern = model_to_dict(item)
        self.assertEqual(pattern, serial(item))

    def test_unknowns(self):
        self.assertEqual(str(Mock), serial(Mock))
