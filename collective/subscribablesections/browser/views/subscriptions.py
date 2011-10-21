from zope.app.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from collective.subscribablesections.interfaces import ISubscribableSection
from collective.subscribablesections.manager import SubscriptionsManager

class MySubscriptions(BrowserView):
    """View own subscriptions
    """

    def __init__(self, *args, **kwargs):
        super(MySubscriptions, self).__init__(*args, **kwargs)
        self.mtool = getToolByName(self.context, 'portal_membership')
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.site = getSite()

    def data(self):
        """Return a dictionary of requests and subscriptions.

        mydict = {
            'requests': [
                {   'title': '',
                    'url': '',
                    'description': '',
                },
            ],
            'subscriptions': [
                # the same...
            ],
        }
        """
        user_id = self.mtool.getAuthenticatedMember().id
        mydict = {
            'requests': [],
            'subscriptions': [],
        }
        query = {
            'object_provides': ISubscribableSection.__identifier__,
            'sort_on' : 'sortable_title',
            'full_objects': True,
            }
        brains = self.catalog.unrestrictedSearchResults(**query)
        for brain in brains:
            title = brain.Title
            url = brain.getURL()
            description = brain.Description
            relative_path = brain.getPath().split('/')[2:]
            obj = self.site.unrestrictedTraverse(relative_path)
            sm = SubscriptionsManager(obj)
            if sm.checkRequestForUser(user_id):
                mydict['requests'].append({
                    'title': title, 'url': url, 'description': description,
                    })
            if sm.checkSubscriptionForUser(user_id):
                mydict['subscriptions'].append({
                    'title': title, 'url': url, 'description': description,
                    })

        return mydict
