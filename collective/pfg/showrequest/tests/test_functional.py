from Products.CMFCore.utils import getToolByName
from Testing import ZopeTestCase as ztc
from collective.pfg.showrequest.tests import base

import doctest
import unittest


class TestSetup(base.FunctionalTestCase):

    def afterSetUp(self):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
        wftool = getToolByName(self.portal, 'portal_workflow')
        self.portal.invokeFactory(
            'FormFolder',
            'form01',
            title="Form01",
            thanksPageOverride='traverse_to:string:form02',
        )
        form01 = self.portal.form01
        form01.actionAdapter = ()
        wftool.doActionFor(form01, "publish")
        form01.reindexObject()
        self.portal.invokeFactory(
            'FormFolder',
            'form02',
            title="Form02",
            thanksPageOverride='traverse_to:string:form2',
        )
        form02 = self.portal.form02
        wftool.doActionFor(form02, "publish")
        form02.reindexObject()
        del form02['thank-you']
        del form02['mailer']


def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/functional.txt',
            package='collective.pfg.showrequest',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ])
