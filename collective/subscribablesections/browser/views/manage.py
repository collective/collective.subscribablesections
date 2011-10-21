from Products.statusmessages.interfaces import IStatusMessage
from Products.Five import BrowserView

from collective.subscribablesections import addStatus
from collective.subscribablesections.config import \
    MESSAGE_MANAGEMENT_FORM_SUCCESS
from collective.subscribablesections.manager import SubscriptionsManager

class ManageSubscriptions(BrowserView):
    """View and manage requests and subscriptions.
    """
        
    def __init__(self, *args, **kwargs):
        super(ManageSubscriptions, self).__init__(*args, **kwargs)
        self.manager = SubscriptionsManager(self.context)
        self.messages = IStatusMessage(self.request)

    def requests(self):
        return self.manager.getRequests()

    def subscriptions(self):
        return self.manager.getSubscriptions()

    def table_data(self):
        """Used to generate the form and parse it.
        """
        tables = {  
            'requests': {
                'button_name': 'form.button.requests', 
                'columns': [
                    {   'id': 'approve', 
                        'name': 'Approve request'}, 
                    {   'id': 'remove', 
                        'name': 'Remove request'},
                    ],
                },
            'subscriptions': {
                'button_name': 'form.button.subscriptions', 
                'columns': [
                    {   'id': 'remove', 
                        'name': 'Remove subscription'},
                ],
            },
        }
        return tables

    def processForm(self):
        form = self.request.form
        table_data = self.table_data()
        # check for submitted form: button name should match the one in table 
        # data
        button_names = [ table_data[key]['button_name'] for key in \
                                                                table_data.keys() ]
        if len(set(form.keys()) & set(button_names)) > 0:
            # process requests
            if form.has_key(table_data['requests']['button_name']):
                # approve subscription requests
                for user_id in form.get('users.id.approve', []):
                    message = self.manager.confirmSubscription(user_id)
                    addStatus(self.request, message)
                # remove subscription requests
                for user_id in form.get('users.id.remove', []):
                    message = self.manager.removeRequest(user_id)
                    addStatus(self.request, message)
            if form.has_key(table_data['subscriptions']['button_name']):
                # remove subscriptions
                for user_id in form.get('users.id.remove', []):
                    message = self.manager.removeSubscription(user_id)
                    addStatus(self.request, message)
            # redirect in order to show status message
            self.request.RESPONSE.redirect(self.request.URL)
        else:
            # no form submitted, do nothing
            pass

