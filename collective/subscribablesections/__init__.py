from zope.i18nmessageid import MessageFactory

import p4a.z2utils # Patch CMFDynamicViewFTI 

MessageFactory = MessageFactory('collective.subscribablesections')
import manager # XXX DEBUG Check syntax on startup

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

