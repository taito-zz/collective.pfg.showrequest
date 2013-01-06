from doctest import DocFileSuite
from doctest import ELLIPSIS
from doctest import NORMALIZE_WHITESPACE
from doctest import REPORT_ONLY_FIRST_FAILURE
from zope.component import testing

import unittest


OF = REPORT_ONLY_FIRST_FAILURE | NORMALIZE_WHITESPACE | ELLIPSIS


def test_suite():
    return unittest.TestSuite([

        DocFileSuite(
            'tests/unittest/browser.txt', package='collective.pfg.showrequest',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=OF), ])
