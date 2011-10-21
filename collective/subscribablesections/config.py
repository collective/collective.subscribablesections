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
# This message is displayed to the Member (on Open Sections, after automatic approval)
MESSAGE_SUBSCRIPTION_GRANTED = (
    _( u'subscription_granted', 
       default = u'You\'re subscribed.' ),
    {'type':"info"} )
# This message is displayed to the Manager (on Closed Sections, after approval)
MESSAGE_SUBSCRIPTION_APPROVED = (
    _( u'subscription_granted', 
       default = u'Subscription was granted.' ),
    {'type':"info"} )
MESSAGE_MANAGEMENT_FORM_SUCCESS = (
    _( u'management_form_success',
       default = u'Form updated.' ),
    {'type': "info"} )
MESSAGE_REQUEST_REMOVED = (
    _( u'request_removed',
       default = u'Request removed.' ),
    {'type': "info"} )
MESSAGE_SUBSCRIPTION_REMOVED = (
    _( u'subscription_removed',
       default = u'Subscription removed.' ),
    {'type': "info"} )

