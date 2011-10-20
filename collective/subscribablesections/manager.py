from DateTime import DateTime

from zope.annotation.interfaces import IAnnotations

from collective.subscribablesections.config import \
    REQUESTS_KEY, SUBSCRIPTIONS_KEY, MESSAGE_REQUEST_EXISTS, \
    MESSAGE_REQUEST_ADDED, MESSAGE_SUBSCRIPTION_GRANTED

"""Annotation storage for subscriptions on Folder items.

We should take care not to define custom classes, as these will break when code
is removed, making it harder to cleanly uninstall the product. So we only use
Python's own classes (lists and dicts) and Zope's (DateTime).

"""

class SubscriptionsManager(object):
    """Various functions to manage requests and subscriptions on one Section
    """

    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(context)
        if not self.annotations.has_key(REQUESTS_KEY):
            self.annotations[REQUESTS_KEY] = []
        if not self.annotations.has_key(SUBSCRIPTIONS_KEY):
            self.annotations[SUBSCRIPTIONS_KEY] = []
        self.requests = self.annotations[REQUESTS_KEY]
        self.subscriptions = self.annotations[SUBSCRIPTIONS_KEY]

    def addRequest(self, user_id):
        if [ r for r in self.annotations[REQUESTS_KEY] if \
                                                    r['user_id'] == user_id]:
            message = MESSAGE_REQUEST_EXISTS
        else:
            self.requests.append(
                {   'user_id': user_id,
                    'request_date': DateTime(),
                    }
            )
            message = MESSAGE_REQUEST_ADDED
        return message

    def _subscribeMember(self, user_id):
        """Add the local role
        """
        roles_tuple = self.context.get_local_roles_for_userid(user_id)
        roles_set = set(roles_tuple)
        roles_set = roles_set.union(set(['Reader']))
        roles_list = list(roles_set)
        self.context.manage_setLocalRoles(user_id, roles_list)
        self.subscriptions.append({   
            'user_id': user_id,
            'subscription_date': DateTime(),
        })

    def grantRequest(self, user_id):
        """Subscribe Member and remove subscription
        """
        self._subscribeMember(user_id)
        return MESSAGE_SUBSCRIPTION_GRANTED

    def immediatelySubscribeMember(self, user_id):
        """Subscribe Member, nothing else.
        """
        self._subscribeMember(user_id)
        return MESSAGE_SUBSCRIPTION_GRANTED
