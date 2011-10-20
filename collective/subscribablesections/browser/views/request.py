from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from collective.subscribablesections import MessageFactory as _
from collective.subscribablesections.interfaces import IClosedSection, \
                                                       IOpenSection
from collective.subscribablesections.manager import SubscriptionsManager

class RequestSubscription(BrowserView):
    """View for requesting Section subscription.
    """

    def __init__(self, *args, **kwargs):
        super(RequestSubscription, self).__init__(*args, **kwargs)
        self.manager = SubscriptionsManager(self.context)
        self.messages = IStatusMessage(self.request)

    def _addStatus(self, message):
        """Message is a tuple containing translated text (message[0]) and a
        dictionary of which we compose keyword arguments (message[1]), like
        message type. They're defined in config.py.
        """
        self.messages.addStatusMessage(message[0], **message[1])

    def __call__(self, *args, **kwargs):
        """Handle subscription request.

        If the context is an Open Section, approve immediately.
        If the context is a Closed Section, send approval and redirect to
        "My Subscriptions" (where the request will show).
        """
        member_id = self.context.portal_membership.getAuthenticatedMember().id
        if IOpenSection.providedBy(self.context):
            # message = self.manager.subscribe(member_id)
            self.messages.addStatusMessage(u"Lala", type="info")        
        else:
            if IClosedSection.providedBy(self.context):
                message = self.manager.addRequest(member_id)
                self._addStatus(message)
                redirect_url = self.context.portal_url() + '/@@my-subscriptions'
                self.request.RESPONSE.redirect(redirect_url)
            else:
                message = """The folder is marked as a Subscribable
Section, but doesn't seem to be of the type Closed Section 
or Open Section."""
                raise Exception(message)
