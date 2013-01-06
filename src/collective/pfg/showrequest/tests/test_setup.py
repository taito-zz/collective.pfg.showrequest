from Products.CMFCore.utils import getToolByName
from collective.pfg.showrequest.tests.base import IntegrationTestCase


class TestSetup(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.actions = getToolByName(self.portal, 'portal_actions')

    def test_is_pfg_installed(self):
        self.failUnless(self.installer.isProductInstalled('PloneFormGen'))

    def test_is_pfg_payment_installed(self):
        self.failUnless(self.installer.isProductInstalled('collective.pfg.showrequest'))

    ## actions.xml
    def test_show_request(self):
        action = self.actions.object_buttons.show_request
        self.assertEqual('Show Request', action.getProperty('title'))
        self.assertEqual('string:${globals_view/getCurrentObjectUrl}/@@show-request', action.getProperty('url_expr'))
        self.assertEqual('python: object.restrictedTraverse("can-show-request")()', action.getProperty('available_expr'))
        self.assertEqual(('Modify portal content',), action.getProperty('permissions'))
        self.assertEqual(True, action.getProperty('visible'))

    def test_not_show_request(self):
        action = self.actions.object_buttons.not_show_request
        self.assertEqual('Not Show Request', action.getProperty('title'))
        self.assertEqual('string:${globals_view/getCurrentObjectUrl}/@@not-show-request', action.getProperty('url_expr'))
        self.assertEqual('python: object.restrictedTraverse("can-hide-request")()', action.getProperty('available_expr'))
        self.assertEqual(('Modify portal content',), action.getProperty('permissions'))
        self.assertEqual(True, action.getProperty('visible'))

    def test_edit_show_request(self):
        action = self.actions.object.edit_show_request
        self.assertEqual('Edit Show Request', action.getProperty('title'))
        self.assertEqual('string:${object_url}/@@edit-show-request', action.getProperty('url_expr'))
        self.assertEqual('python: object.restrictedTraverse("can-hide-request")()', action.getProperty('available_expr'))
        self.assertEqual(('Modify portal content',), action.getProperty('permissions'))
        self.assertEqual(True, action.getProperty('visible'))

    ## Uninstalling
    def test_uninstall(self):
        self.installer.uninstallProducts(['collective.pfg.showrequest'])
        self.failUnless(not self.installer.isProductInstalled('collective.pfg.showrequest'))
        self.failIf(hasattr(self.actions.object_buttons, 'show_request'))
        self.failIf(hasattr(self.actions.object_buttons, 'not_show_request'))
        self.failIf(hasattr(self.actions.object, 'edit_show_request'))
