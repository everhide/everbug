import sys
from unittest import TestCase

from everbug.shortcuts import profile
from everbug.utils.manager import ProfileManager


class TestProfile(TestCase):

    @classmethod
    def setUp(cls):
        cls.manager = ProfileManager()

    @profile
    def target(self):
        import inspect
        return inspect.stack()

    @profile(short=False)
    def target_with_arg(self):
        import inspect
        return inspect.stack()

    def test_arg_default(self):
        self.manager.clear()
        self.target()
        self.assertEqual(len(self.manager.profiles()[0]['lines']), 20)

    def test_arg_custom(self):
        self.manager.clear()
        self.target_with_arg()
        self.assertGreater(len(self.manager.profiles()[0]['lines']), 20)

    def test_field_method(self):
        self.manager.clear()
        self.target()
        origin_name = self.target.__name__
        profiled_name = self.manager.profiles()[0]['method']
        self.assertEqual(origin_name, profiled_name)

    def test_field_module(self):
        self.manager.clear()
        self.target()
        origin_name = sys.modules[self.target.__module__].__file__
        profiled_name = self.manager.profiles()[0]['module']
        self.assertEqual(origin_name, profiled_name)
