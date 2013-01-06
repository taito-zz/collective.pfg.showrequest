from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from collective.pfg.showrequest.interfaces import IShowRequest
from zope.interface import alsoProvides, noLongerProvides


class Miscellaneous(BrowserView):

    def show_request(self):
        context = aq_inner(self.context)
        if IPloneFormGenForm.providedBy(context):
            alsoProvides(context, IShowRequest)
            url = '{}/@@edit-show-request'.format(context.absolute_url())
            return self.request.response.redirect(url)

    def not_show_request(self):
        context = aq_inner(self.context)
        noLongerProvides(context, IShowRequest)
        return self.request.response.redirect(context.absolute_url())

    def can_show_request(self):
        context = aq_inner(self.context)
        return IPloneFormGenForm.providedBy(context) and not IShowRequest.providedBy(context)

    def can_hide_request(self):
        context = aq_inner(self.context)
        return IPloneFormGenForm.providedBy(context) and IShowRequest.providedBy(context)
