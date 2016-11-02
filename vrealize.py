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
            message_object = read_json(message)
        elif content_type == 'application/xml':
            raise NotImplemented
        else:
            raise NotImplemented
        
        self.startDate = message_object.get('startDate', None)
        self.criticality = message_object.get('criticality', None)
        self.resourceId = message_object.get('resourceId', None)
        self.alertId = message_object.get('alertId', None)
        self.status = message_object.get('status', None)
        self.subType = message_object.get('subType', None)
        self.cancelDate = message_object.get('cancelDate', None)
        self.resourceKind = message_object.get('resourceKind', None)
        self.adapterKind = message_object.get('adapterKind', None)
        self.type = message_object.get('type', None)
        self.resourceName = message_object.get('resourceName', None)
        self.updateDate = message_object.get('updateDate', None)
        self.info = message_object.get('info', None)


    def read_json(self, message):
        return json.load(message)


    # TODO:
    def read_xml(self, message):
        return False
