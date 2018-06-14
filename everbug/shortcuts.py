import sys
from cProfile import Profile
from functools import partial, wraps

from everbug.utils.manager import ProfileManager
from everbug.utils.pstats import StatsDict


def profile(method=None, *, short=True):
    if not method:
        return partial(profile, short=short)

    manager = ProfileManager()

    @wraps(method)
    def wrapper(*args, **kwargs):
        prof = Profile()
        try:
            prof.enable()
            execute = method(*args, **kwargs)
            prof.disable()
            return execute
        finally:
            stats = StatsDict(prof)
            prof_data = stats.sort_stats('cumtime').dump(short)
            prof_data['method'] = method.__name__
            prof_data['module'] = sys.modules[method.__module__].__file__
            manager.add(prof_data)
    return wrapper
