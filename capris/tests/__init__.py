import os
import unittest
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
from capris import Command

__all__ = ['CaprisTest']


class Helpers(object):
    @property
    def stringio(self):
        return StringIO

    def assert_ok(self, response):
        assert response.status_code == 0

    def last_response(self, transaction):
        return transaction.results[-1]


class CaprisTest(unittest.TestCase):
    helpers = Helpers()

    def setUp(self):
        self.grep = Command('grep')
        self.cat = Command('cat')
        self.ls = Command('ls')


def get_tests():
    import capris.tests
    modules = [m[:-3] for m in os.listdir(capris.tests.__path__[0])
               if not m.startswith('__')
               and m.endswith('.py')]
    loader = unittest.TestLoader()

    for item in modules:
        module = 'capris.tests.{package}'.format(package=item)
        testcase = loader.loadTestsFromName(module)
        yield testcase
