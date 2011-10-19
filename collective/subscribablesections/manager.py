from DateTime import DateTime

from zope.annotation.interfaces import IAnnotations

from collective.subscribablesections import MessageFactory as _
from collective.subscribablesections.config import REQUESTS_KEY, \
                                                   SUBSCRIPTIONS_KEY

"""Annotation storage for subscriptions on Folder items.

We should take care not to define custom classes, as these will break when code
is removed, making it harder to cleanly uninstall the product. So we only use
Python's own classes (lists and dicts) and Zope's (DateTime).

"""

class SubscriptionsManager(object):
    """Various functions to manage requests and subscriptions on one Section
    """

    def __init__(self, context):
        self.annotations = IAnnotations(context)
        if not self.annotations.has_key(REQUESTS_KEY):
            self.annotations[REQUESTS_KEY] = []
        if not self.annotations.has_key(SUBSCRIPTIONS_KEY):
            self.annotations[SUBSCRIPTIONS_KEY] = []

    def getRequests(self):
        return self.annotations[REQUESTS_KEY]

    def getSubscriptions(self):
        return self.annotations[SUBSCRIPTIONS_KEY]

    def addRequest(self, user_id):
        if [ r for r in self.annotations[REQUESTS_KEY] if \
                                                    r['user_id'] == user_id]:
            message = _(u'request_exists', 
                        default = u'Subscription request exists for this user.')
        else:
            self.annotations[REQUESTS_KEY].append(
                {   'user_id': user_id,
                    'request_date': DateTime(),
                    }
            )
            message =_(u'request_added', 
                       default = u'Your subscription request was added.')
        print(message) # XXX DEBUG
        return message
