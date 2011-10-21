from DateTime import DateTime

from zope.annotation.interfaces import IAnnotations

from collective.subscribablesections.config import \
    REQUESTS_KEY, SUBSCRIPTIONS_KEY, MESSAGE_REQUEST_EXISTS, \
    MESSAGE_REQUEST_ADDED, MESSAGE_SUBSCRIPTION_GRANTED, \
    MESSAGE_SUBSCRIPTION_APPROVED, MESSAGE_SUBSCRIPTION_REMOVED, \
    MESSAGE_REQUEST_REMOVED
from collective.subscribablesections.interfaces import ISubscribableSection

"""Annotation storage for subscriptions on Folder items.

We should take care not to define custom classes, as these will break when code
is removed, making it harder to cleanly uninstall the product. So we only use
Python's own classes (lists and dicts) and Zope's (DateTime).

"""

class SubscriptionsManager(object):
    """Various functions to manage requests and subscriptions on one Section
    """

    def __init__(self, context):
        assert ISubscribableSection.providedBy(context) # XXX DEBUG
        self.context = context

    def getRequests(self):
        return IAnnotations(self.context).get(REQUESTS_KEY, [])

    def getSubscriptions(self):
        return IAnnotations(self.context).get(SUBSCRIPTIONS_KEY, [])

    def addRequest(self, user_id):
        requests = self.getRequests()
        if [ r for r in requests if r['user_id'] == user_id]:
            message = MESSAGE_REQUEST_EXISTS
        else:
            requests.append(
                {   'user_id': user_id,
                    'date': DateTime(),
                    }
            )
            message = MESSAGE_REQUEST_ADDED
            IAnnotations(self.context)[REQUESTS_KEY] = requests
        return message

    def _subscribeMember(self, user_id):
        """Add the local role, and keep track of subscription also in our
        Annotation storage.

        Before adding the subscription to the subscriptions list, we remove 
        any existing entries for the user_id.

        """
        roles_tuple = self.context.get_local_roles_for_userid(user_id)
        roles_set = set(roles_tuple)
        roles_set = roles_set.union(set(['Reader']))
        roles_list = list(roles_set)

        self.context.manage_setLocalRoles(user_id, roles_list)
        subscriptions = self.getSubscriptions()
        subscriptions = [s for s in subscriptions if s['user_id'] != user_id]
        subscriptions.append({   
            'user_id': user_id,
            'date': DateTime(),
        })
        IAnnotations(self.context)[SUBSCRIPTIONS_KEY] = subscriptions

        # Remove request
        self._removeRequest(user_id)

    def _removeRequest(self, user_id):
        """ Remove requests from requests list. Should not give an error if user_id is
        not found.
        """
        requests = self.getRequests()
        requests = [r for r in requests if r['user_id'] != user_id]
        IAnnotations(self.context)[REQUESTS_KEY] = requests

    def confirmSubscription(self, user_id):
        """Confirm subscription to Closed Group, return message to Manager
        """
        self._subscribeMember(user_id)
        return MESSAGE_SUBSCRIPTION_APPROVED

    def immediatelySubscribeMember(self, user_id):
        """Subscribe Member to Open Section, return message to Member
        """
        self._subscribeMember(user_id)
        return MESSAGE_SUBSCRIPTION_GRANTED

    def removeRequest(self, user_id):
        """Remove request, return message
        """
        self._removeRequest(user_id)
        return MESSAGE_REQUEST_REMOVED

    def _removeSubscription(self, user_id):
        """Remove subscription from list, remove Role.
        """
        roles_tuple = self.context.get_local_roles_for_userid(user_id)
        roles_set = set(roles_tuple)
        roles_set = roles_set - set(['Reader'])
        roles_list = list(roles_set)
        if roles_list:
            self.context.manage_setLocalRoles(user_id, roles_list)
        else:
            self.context.manage_delLocalRoles([user_id])


        subscriptions = self.getSubscriptions()
        subscriptions = [s for s in subscriptions if s['user_id'] != user_id]
        IAnnotations(self.context)[SUBSCRIPTIONS_KEY] = subscriptions

    def removeSubscription(self, user_id):
        """Remove subscription, return message
        """
        self._removeSubscription(user_id)
        return MESSAGE_SUBSCRIPTION_REMOVED
