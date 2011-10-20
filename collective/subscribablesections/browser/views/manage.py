from Products.Five import BrowserView
from collective.subscribablesections.manager import SubscriptionsManager

class ManageSubscriptions(BrowserView):
    """View and manage requests and subscriptions.
    """
        
    def __init__(self, *args, **kwargs):
        super(ManageSubscriptions, self).__init__(*args, **kwargs)
        self.manager = SubscriptionsManager(self.context)

    def requests(self):
        return self.manager.requests

    def subscriptions(self):
        return self.manager.subscriptions
