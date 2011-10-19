from Acquisition import aq_inner

from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.subscribablesections import MessageFactory as _
from collective.subscribablesections.interfaces import ISubscribableSection

class ISubscribableSectionsPortlet(IPortletDataProvider):
    pass

class Assignment(base.Assignment):
    implements(ISubscribableSectionsPortlet)

    @property
    def title(self):
        return _(u"Subscribable sections")

class AddForm(base.AddForm):
    form_fields = form.Fields(ISubscribableSectionsPortlet)
    label = _(u"Add Subscribable Sections portlet")
    description = _(u"This portlet lists Subscribable Sections in the site.")

    def create(self, data):
        return Assignment()

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('sections.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()  # whether or not the current user is Anonymous

        plone_tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.catalog = plone_tools.catalog()

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements."""
        return not self.anonymous and len(self._data())

    def sections(self):
        return self._data()

    @property
    def title(self):
        return Assignment().title

    @memoize
    def _data(self):
        query = {
            'object_provides': ISubscribableSection.__identifier__,
            'sort_on' : 'sortable_title',
            }
        results = self.catalog.unrestrictedSearchResults(**query)
        return results
