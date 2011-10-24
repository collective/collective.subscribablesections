from AccessControl import getSecurityManager
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from Products.CMFCore import permissions
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from collective.subscribablesections import MessageFactory as _
from collective.subscribablesections.interfaces import ISubscribableSection
from collective.subscribablesections.manager import SubscriptionsManager

class ISubscribableRequestsPortlet(IPortletDataProvider):
    pass

class Assignment(base.Assignment):
    implements(ISubscribableRequestsPortlet)

    @property
    def title(self):
        return _(u"Subscription requests")

class AddForm(base.AddForm):
    form_fields = form.Fields(ISubscribableRequestsPortlet)
    label = _(u"Add Subscription Requests portlet")
    description = _(u"This portlet lists all requested subscriptions in the site.")

    def create(self, data):
        return Assignment()

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('requests.pt')

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
        """Show the portlet only: to users who are logged in, if there are one 
        or more Susbscribable Sections
        """
        return not self.anonymous and len(self._data())

    def requests(self):
        return self._data()

    @property
    def title(self):
        return Assignment().title

    def _compareRequestDates(self, req1, req2):
        """Comparison function to sort list of requests in order of request
        date (ascending, ie. olderst first). 
        """
        if req1['date'] > req2['date']:
            return 1
        if req1['date'] < req2['date']:
            return -1
        return 0
        
    @memoize
    def _data(self):
        """Returns a list of all pending subscription requests, adding the URL,
        description and title of the Section they're for.
        """
        query = {
            'object_provides': ISubscribableSection.__identifier__,
            'sort_on' : 'sortable_title',
            }
        results = self.catalog.unrestrictedSearchResults(**query)
        all_requests = []
        for brain in results:
            section = brain.getObject()
            if getSecurityManager().checkPermission(
                    permissions.ManagePortal, section):
                manager = SubscriptionsManager(section)
                requests = manager.getRequests()
                for r in requests:
                    r['title'] = brain.Title
                    r['description'] = brain.Description
                    r['url'] = brain.getURL()
                    all_requests.append(r)
        all_requests.sort(self._compareRequestDates) 
        return all_requests
