from unittest import TestCase

from everbug.utils.manager import ProfileManager


class TestProfileManager(TestCase):

    @classmethod
    def setUp(cls):
        cls.manager = ProfileManager()

    def test_single_instance(self):
        self.assertEqual(id(self.manager), id(ProfileManager()))

    def test_append(self):
        self.manager.clear()
        self.manager.add('item')
        self.assertEqual(self.manager.profiles()[0], 'item')

    def test_count(self):
        self.manager.clear()
        for i in range(0, 10):
            self.manager.add('item_%s' % i)
        self.assertEqual(self.manager.count, 10)
