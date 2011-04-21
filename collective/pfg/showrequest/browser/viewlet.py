#from zope.annotation import IAnnotations
#from zope.component import getMultiAdapter
#from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
#from Products.CMFCore.utils import getToolByName
#from Products.CMFCore.interfaces import ISiteRoot
from Products.PloneFormGen.interfaces import IPloneFormGenThanksPage
#from collective.pfg.payment.interfaces import (
#    IProperties,
#)


class ShowRequestViewlet(ViewletBase):

    index = render = ViewPageTemplateFile("viewlets/show_request.pt")

    def all_fields(self):
        thanks = [obj for obj in self.context.objectValues() if IPloneFormGenThanksPage.providedBy(obj)]
        if thanks:
            return thanks[0].displayInputs(self.request)


#    @property
#    def current_url(self):
#        """Returns current url"""
#        context_state = getMultiAdapter((self.context, self.request),
#                                            name=u'plone_context_state')
#        return context_state.current_page_url()
