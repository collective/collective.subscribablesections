from Products.Five import BrowserView

from collective.subscribablesections.manager import SubscriptionsManager
from collective.subscribablesections import MessageFactory as _

class RequestSubscription(BrowserView):
    """Form to request section subscription.
    """

    def __init__(self, *args, **kwargs):
        super(RequestSubscription, self).__init__(*args, **kwargs)
        self.manager = SubscriptionsManager(self.context)

    def __call__(self, *args, **kwargs):
        """Redirect immediately, no view template
        """
        member_id = self.context.portal_membership.getAuthenticatedMember().id
        message = self.manager.addRequest(member_id)
        redirect_url = self.context.portal_url() + '/@@my-subscriptions'
        self.request.RESPONSE.redirect(redirect_url)
