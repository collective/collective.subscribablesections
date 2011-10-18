from Products.Five import BrowserView
from collective.subscribablesections.interfaces import IClosedSection, \
                                                       IOpenSection

class SubscribableSections(BrowserView):
    """Helper view class for subcribable sections.
    """
    
    def check_came_from(self):
        """Check if object requires a subscription to view.
        Because we lost our original context during redirect, we get the
        original object from the came_from value.
        """
        if self.request.has_key('came_from'):
            came_from = self.request['came_from'].split('/')
            portal_url = self.context.portal_url().split('/')
            # get relative path
            while portal_url and came_from and came_from[0] == portal_url[0]:
                came_from.pop(0)
                portal_url.pop(0)
            view_url = '/'.join(came_from) + '/@@subscribable_sections_view'
            self.context.plone_log(view_url)
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
