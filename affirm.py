# affirm.py / Eli Finer / 2016
#
# This script causes assert statements to output much better default error messages
# that include the tested condition and the values for any variables referenced in it.
#
# Here are some examples:
#
# >>> assert 1 > 2
# AssertionError: assertion (1 > 2) failed
#
# >>> a = 1; b = 2; c = 'foo'; d = None
# >>> assert a > b
# AssertionError: assertion (a > b) failed with a=1, b=2
#
# >>> assert c is None
# AssertionError: assertion (c is None) failed with c='foo'
#
# >>> assert a == b == c
# AssertionError: assertion (a == b == c) failed with a=1, b=2, c='foo'

import re
import ast
import types
import inspect
from collections import OrderedDict

def make_assert_message(frame, regex):
    class ReferenceFinder(ast.NodeVisitor):
        def __init__(self):
            self.names = []
        def find(self, tree, frame):
            self.visit(tree)
            nothing = object()
            deref = OrderedDict()
            for name in self.names:
                value = frame.f_locals.get(name, nothing) or frame.f_globals.get(name, nothing)
                if value is not nothing and not isinstance(value, (types.ModuleType, types.FunctionType)):
                    deref[name] = repr(value)
            return deref
        def visit_Name(self, node):
            self.names.append(node.id)

    code_context = inspect.getframeinfo(frame)[3]
    if not code_context:
        return ''
    match = re.search(regex, code_context[0])
    if not match:
        return ''
    condition = match.group(1).strip()
    deref = ReferenceFinder().find(ast.parse(condition), frame)
    deref_str = ''
    if deref:
        deref_str = ' with ' + ', '.join('{}={}'.format(k, v) for k, v in deref.items())
    return 'assertion {} failed{}'.format(condition, deref_str)

import sys
_old_excepthook = sys.excepthook
def assert_excepthook(type, value, traceback):
    if type == AssertionError:
        from traceback import print_exception
        if not value.args:
            top = traceback
            while top.tb_next and top.tb_next.tb_frame:
                top = top.tb_next
            message = make_assert_message(top.tb_frame, r'assert\s+([^#]+)')
            value = AssertionError(message)
        print_exception(type, value, traceback)
    else:
        _old_excepthook(type, value, traceback)
sys.excepthook = assert_excepthook

def affirm(condition):
    if not __debug__:
        return
    if condition:
        return
    else:
        message = make_assert_message(inspect.currentframe().f_back, r'affirm\s*\(\s*(.+)\s*\)')
        raise AssertionError(message)
