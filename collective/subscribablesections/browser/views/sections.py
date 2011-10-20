from Products.Five import BrowserView
from collective.subscribablesections.interfaces import IClosedSection, \
                                                       IOpenSection

class SubscribableSectionsView(BrowserView):
    """Helper view class for subcribable sections.
    """
    
    def check_came_from(self):
        """Check if redirecting object requires a subscription to view.

        Because this method is called from the context of 
        /Plone/acl_users/credentials_cookie_auth, we compose the original
        object's relative path from the came_from value and the portal_url. 

        We then call this view's 'subscription_required' method on the original
        object.

        """
        if self.request.has_key('came_from'):
            self.came_from = self.request['came_from']
            came_from = self.came_from
            portal_url = self.context.portal_url()
            relative_came_from = came_from.replace(portal_url, '').lstrip('/')
            self.came_from_obj = self.context.unrestrictedTraverse(
                relative_came_from)
            view_url = relative_came_from + '/@@subscribable-sections-view'
            view = self.context.unrestrictedTraverse(view_url)
            return view.subscription_required()
        return False
            
    def subscription_required(self):
        """Check if object requires a subscription to view.
        """
        for interface in [IClosedSection, IOpenSection]:
            if interface.providedBy(self.context):
                return True
        return False

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
