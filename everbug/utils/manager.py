class _Manager(type):
    """ Singletone for cProfile manager """
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(_Manager, cls).__call__(*args, **kwargs)
        return cls._inst[cls]


class ProfileManager(metaclass=_Manager):

    def __init__(self):
        self._profiles = list()

    def clear(self):
        self._profiles.clear()

    def add(self, profile):
        self._profiles.append(profile)

    def profiles(self):
        return self._profiles

    @property
    def count(self):
        return len(self._profiles)
