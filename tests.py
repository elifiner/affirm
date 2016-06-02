import os
import sys
import subprocess
import unittest

# Tests are executed in a separate Python process because there's no way to capture
# the excepthook results within the same process (we need to let the exception fall
# through to the interpreter to get it to the excepthook.)
#
# This is ugly but it works.

TEMPFILE = '_temp_test.py'

SOURCE = '''
import affirm
a = 1
b = 2
c = None
d = 'foo'
{statement}
'''

class TestAssert(unittest.TestCase):
    def __init__(self, statement, expected_message, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.statement = statement
        self.expected_message = expected_message

    def runTest(self):
        with open(TEMPFILE, 'w') as f:
            f.write(SOURCE.format(statement=self.statement))
        result = subprocess.run([sys.executable, TEMPFILE], stderr=subprocess.PIPE)
        assert_message = result.stderr.decode('utf8').splitlines()[-1]
        self.assertEqual(assert_message, self.expected_message)

    def __str__(self):
        return self.statement

suite = unittest.TestSuite()
def test(statement, expected_message):
    suite.addTest(TestAssert(statement, expected_message))

test('assert 1 > 2', 'AssertionError: assertion (1 > 2) failed')
test('assert a > b', 'AssertionError: assertion (a > b) failed with a=1, b=2')
test('assert a + b > a + b * 2', 'AssertionError: assertion (a + b > a + b * 2) failed with a=1, b=2')
test('assert a is None', 'AssertionError: assertion (a is None) failed with a=1')
test('assert c is not None', 'AssertionError: assertion (c is not None) failed with c=None')
test('assert d == "bar"', 'AssertionError: assertion (d == "bar") failed with d=\'foo\'')

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
    os.unlink(TEMPFILE)
