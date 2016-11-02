# vRealize alert message object to handle JSON and XML in a unified way.
# Not been able to test XML yet so it's not implemented. Would be best to
# use the builtin lxml.etree.ElementTree parser.

import json

class VRealizeAlert(object):

    def __init__(self, message, **kw):
        """
        message argument is a StringIO buffer
        """

        content_type = kw.get('content_type', 'application/json')

        if content_type == 'application/json':
            message_data = self._read_json(message)
        elif content_type == 'application/xml':
            raise NotImplemented
        else:
            raise NotImplemented
        
        self.startDate = message_data.get('startDate', None)
        self.criticality = message_data.get('criticality', None)
        self.resourceId = message_data.get('resourceId', None)
        self.alertId = message_data.get('alertId', None)
        self.status = message_data.get('status', None)
        self.subType = message_data.get('subType', None)
        self.cancelDate = message_data.get('cancelDate', None)
        self.resourceKind = message_data.get('resourceKind', None)
        self.adapterKind = message_data.get('adapterKind', None)
        self.type = message_data.get('type', None)
        self.resourceName = message_data.get('resourceName', None)
        self.updateDate = message_data.get('updateDate', None)
        self.info = message_data.get('info', None)

        self.message = message_data


    def _read_json(self, message):
        return json.load(message)


    # TODO:
    def _read_xml(self, message):
        return False


    @property
    def message_data(self):
        return self.message


    @property
    def message_json(self):
        return json.dumps(self.message)
