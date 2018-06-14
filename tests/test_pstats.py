from cProfile import Profile
from unittest import TestCase

from everbug.utils.pstats import StatsDict


class TestStatsDictDump(TestCase):

    def func_with_many_calls(self):
        import inspect
        return inspect.stack()

    def inspect(self, method):
        profile = Profile()
        profile.enable()
        method()
        profile.disable()
        return StatsDict(profile).sort_stats('cumtime')

    def test_lines_default(self):
        stats = self.inspect(self.func_with_many_calls).dump()
        self.assertGreater(len(stats['lines']), 20)

    def test_lines_short(self):
        stats = self.inspect(self.func_with_many_calls).dump(short=True)
        self.assertEqual(len(stats['lines']), 20)

    def test_lines_all(self):
        stats = self.inspect(self.func_with_many_calls).dump(short=False)
        self.assertGreater(len(stats['lines']), 20)

    def test_fields(self):
        stats = self.inspect(self.func_with_many_calls).dump()
        self.assertCountEqual(['lines', 'total_calls', 'total_time'], stats)
