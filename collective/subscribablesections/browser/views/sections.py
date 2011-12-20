from Acquisition import aq_inner
from Products.Five import BrowserView
from collective.subscribablesections.interfaces import IClosedSection, \
                                                       IOpenSection

class SubscribableSectionsView(BrowserView):
    """Helper view class for subcribable sections.
    """

    def __init__(self, context, request):
        """ Try to retrieve the object that's in the came_from attribute
        """
        super(SubscribableSectionsView, self)
        self.context = context
        self.request = request

        self.came_from = self.request.get('came_from')
        self.relative_came_from = None
        self.came_from_obj = None

        if self.came_from:
            relative_came_from = self.came_from.replace(
                context.portal_url(), '').lstrip('/')
            self.came_from_obj = self.context.unrestrictedTraverse(
                relative_came_from)


    def check_came_from(self):
        """Check if redirecting object requires a subscription to view.

        Because this method is called from the context of 
        /Plone/acl_users/credentials_cookie_auth, we compose the original
        object's relative path from the came_from value and the portal_url. 

        We then call this view's 'subscription_required' method on the original
        object.

        """
        if self.came_from_obj:
            return self.subscription_required(self.came_from_obj)

    def subscription_required(self, context=None):
        """Check if object requires a subscription to view.
        """
        if not context:
            context = self.context

        for interface in [IClosedSection, IOpenSection]:
            if interface.providedBy(context):
                return True

    def closed_section_url(self):
        """Return the url of the Subscribable Section.
        """
        return self.came_from

    def title(self):
        """Return the Subscribable Section's title.
        """
        title = self.came_from_obj.Title()

    def description(self):
        """Return the Subscribable Section's description.
        """
        return self.came_from_obj.Description()
