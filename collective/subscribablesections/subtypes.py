from zope.component import provideUtility
from zope.interface import implements

from p4a.subtyper.interfaces import IPortalTypedFolderishDescriptor

from collective.subscribablesections import MessageFactory as _
from interfaces import IClosedSection, IOpenSection

class BaseSectionDescriptor(object):
    implements(IPortalTypedFolderishDescriptor)
    for_portal_type = 'Folder'
    
class ClosedSectionDescriptor(BaseSectionDescriptor):
    title = _(u'Closed Section')
    description = _(u'Folder for which approved subscription is required to view it')
    type_interface = IClosedSection

class OpenSectionDescriptor(BaseSectionDescriptor):
    title = _(u'Open Section')
    description = _(u'Folder for which subscription is required to view it, where subscription is given immediately upon request')
    type_interface = IOpenSection
