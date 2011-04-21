try:
    import unittest2 as unittest
except ImportError:
    import unittest
import doctest
from doctest import (
    DocFileSuite,
    ELLIPSIS,
    NORMALIZE_WHITESPACE,
    REPORT_ONLY_FIRST_FAILURE,
)
from zope.component import testing

OF = REPORT_ONLY_FIRST_FAILURE | NORMALIZE_WHITESPACE | ELLIPSIS


def test_suite():
    return unittest.TestSuite([

        DocFileSuite(
            'tests/unittest/browser.txt', package='collective.pfg.showrequest',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=OF),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
