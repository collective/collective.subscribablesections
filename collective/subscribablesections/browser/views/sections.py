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
            relative_came_from = self.came_from.replace(context.portal_url(), '').lstrip('/')

            ##When using apache2 or other webserver, you usually give a
            ##VirtualHostBase, this means that stripping portal_url from the
            ##came_from results in a 'not deep enough' relative part.
            ##Since VirtualHostBase can be a map deeper in the plone site.
            ##So if we got that in request, we incorporate it into the relative
            ##path.
            virtual_path = list(self.request.get('VirtualRootPhysicalPath', []))

            if virtual_path:
               ##The VirtualRootPhysicalPath goes all the way back to Zope.
               ##We filter out any empty parts and the plone site.
               ##Since we still have the plone site as context.
               ##we're only interest in any folderish items below plone. 
               virtual_path = [part for part in virtual_path \
                                          if part and part !=\
                                              self.context.id] ##self.context.id == Plone Site

               ##Incorporate our virtual_path into the relative_came_from
               if virtual_path:
                   virtual_path = "/".join(virtual_path)
                   relative_came_from = "%s/%s" % (virtual_path, relative_came_from)

            try:
                # the object might have been deleted in the mean time..
                # e.g. in a @@moderate-delete-comment call
                self.came_from_obj = self.context.unrestrictedTraverse(relative_came_from)
            except:
                self.came_from_obj = None


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
        if self.came_from_obj:
            return self.came_from_obj.Title()

    def description(self):
        """Return the Subscribable Section's description.
        """
        if self.came_from_obj:
            return self.came_from_obj.Description()
