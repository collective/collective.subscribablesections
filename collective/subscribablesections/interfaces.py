from zope.interface import Interface

class ISubscribableSection(Interface):
    """A folder that is marked as a "closed group".
    """

class IClosedSection(ISubscribableSection):
    """A folder that is marked as a "closed group".
    """

class IOpenSection(ISubscribableSection):
    """A folder that is marked as an "open group".
    """
