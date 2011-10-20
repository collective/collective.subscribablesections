from collective.subscribablesections import MessageFactory as _

REQUESTS_KEY = "collective.subscribablesections.requests"
SUBSCRIPTIONS_KEY = "collective.subscribablesections.subscriptions"

MESSAGE_REQUEST_EXISTS = (
    _( u'request_exists',
       default = u'Subscription request exists for this user.' ), 
    {'type':"error"} )

MESSAGE_REQUEST_ADDED = (
    _( u'request_added', 
       default = u'Your subscription request was added.' ),
    {'type':"info"} )

# This message can be displayed to the Member (on Open Sections, after request
# and immediate approval) as well as to the Manager (on Closed Sections, after
# approval).
MESSAGE_SUBSCRIPTION_GRANTED = (
    _( u'subscription_granted', 
       default = u'Subscription was granted.' ),
    {'type':"info"} )
