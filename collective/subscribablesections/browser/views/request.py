from Products.Five import BrowserView

from collective.subscribablesections import MessageFactory as _, addStatus
from collective.subscribablesections.interfaces import IClosedSection, \
                                                       IOpenSection
from collective.subscribablesections.manager import SubscriptionsManager

class RequestSubscription(BrowserView):
    """View for requesting Section subscription.
    """

    def __init__(self, *args, **kwargs):
        super(RequestSubscription, self).__init__(*args, **kwargs)
        self.manager = SubscriptionsManager(self.context)

    def __call__(self, *args, **kwargs):
        """Handle subscription request.

        If the context is an Open Section, approve immediately.

        If the context is a Closed Section, send approval and redirect to
        "My Subscriptions" (where the request will show).
        """
        user_id = self.context.portal_membership.getAuthenticatedMember().id
        if IOpenSection.providedBy(self.context):
            message = self.manager.immediatelySubscribeMember(user_id)
            addStatus(self.request, message)        
            self.request.RESPONSE.redirect(self.context.absolute_url())
        else:
            if IClosedSection.providedBy(self.context):
                message = self.manager.addRequest(user_id)
                addStatus(self.request, message)
                redirect_url = self.context.portal_url() + '/@@my-subscriptions'
                self.request.RESPONSE.redirect(redirect_url)
            else:
                message = """The folder is marked as a Subscribable
Section, but doesn't seem to be of the type Closed Section 
or Open Section."""
                raise Exception(message)
