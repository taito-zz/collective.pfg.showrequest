from Acquisition import aq_inner
from Products.Archetypes.interfaces.field import IField
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PloneFormGen import implementedOrProvidedBy
from persistent.list import PersistentList
from plone.app.layout.viewlets.common import ViewletBase
from zope.annotation import IAnnotations
from zope.component import getMultiAdapter


class ShowRequestViewlet(ViewletBase):

    index = render = ViewPageTemplateFile("viewlets/show_request.pt")

    def all_fields(self):
        context = aq_inner(self.context)
        fields = IAnnotations(context).get('collective.pfg.showrequest.fields')
        if fields is not None:
            objs = [
                (obj.id, obj) for obj in context._getFieldObjects() if (
                    not implementedOrProvidedBy(IField, obj) or obj.isLabel()
                ) and obj.id in fields
            ]
            sorted_objs = []
            objs = dict(objs)
            for field in fields:
                sorted_objs.append(objs[field])
            res = []
            for obj in sorted_objs:
                value = obj.htmlValue(self.request)
                res.append({
                    'label': obj.fgField.widget.label,
                    'value': value,
                })
            return res

    def displayInputs(self, request):
        """ Returns sequence of dicts {'label':fieldlabel, 'value':input}
        """
        # get a list of all candidate fields
        myFields = []
        for obj in self.aq_parent._getFieldObjects():
            if (not implementedOrProvidedBy(IField, obj) or obj.isLabel()):
                # if field list hasn't been specified explicitly, exclude server side fields
                if self.showAll and obj.getServerSide():
                    continue
                myFields.append(obj)
        # Now, determine which fields we show
        if self.showAll:
            sFields = myFields
        else:
            sFields = []
            # acquire field list from parent
            res = []
            for id in self.showFields:
                # inefficient if we get many fields
                for f in myFields:
                    if f.getId() == id:
                        sFields.append(f)
                        break

        # Now, build the results list
        res = []
        for obj in sFields:
            value = obj.htmlValue(request)
            if self.includeEmpties or (value and (value != 'No Input')):
                res.append({
                    'label': obj.fgField.widget.label,
                    'value': value,
                })

        return res


class SettingViewlet(ViewletBase):

    index = render = ViewPageTemplateFile("viewlets/setting.pt")

    @property
    def current_url(self):
        """Returns current url"""
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        return context_state.current_page_url()

    def update(self):
        form = self.request.form
        if form.get('form.button.UpdateFields', None) is not None:
            context = aq_inner(self.context)
            fields = form.get('fields')
            if fields != '':
                values = [field.replace(' ', '') for field in fields.split('\r\n')]
                IAnnotations(context)['collective.pfg.showrequest.fields'] = PersistentList(values)

    def fields(self):
        context = aq_inner(self.context)
        fields = IAnnotations(context).get('collective.pfg.showrequest.fields')
        if fields is not None:
            return '\r\n'.join(fields)
