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
