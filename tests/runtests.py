import os
import sys
from unittest import TestSuite, TextTestRunner, defaultTestLoader

from django import setup


TEST_MODULES = (
    'test_profile',
    'test_pstats',
    'test_manager',
    'test_queries',
    'test_context',
    'test_middleware',
    'test_serializer',
)


def run():
    suite = TestSuite()
    for test in TEST_MODULES:
        try:
            mod = __import__(test, globals(), locals(), ['suite'])
            suitefn = getattr(mod, 'suite')
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            suite.addTest(defaultTestLoader.loadTestsFromName(test))
    TextTestRunner().run(suite)


if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.curdir))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'stub.settings'
    setup()
    run()
