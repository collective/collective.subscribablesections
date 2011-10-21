from zope.i18nmessageid import MessageFactory

import p4a.z2utils # Patch CMFDynamicViewFTI 
from Products.statusmessages.interfaces import IStatusMessage

MessageFactory = MessageFactory('collective.subscribablesections')
import manager # XXX DEBUG Check syntax on startup

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

def addStatus(request, message):
    """Message is a tuple containing translated text (message[0]) and a
    dictionary of which we compose keyword arguments (message[1]), like
    message type. Messages are defined in config.py.
    """
    messages = IStatusMessage(request)
    messages.addStatusMessage(message[0], **message[1])

