# vRealize alert message object to handle JSON and XML in a unified way.
# Not been able to test XML yet so it's not implemented. Would be best to
# use the builtin lxml.etree.ElementTree parser.

import json
from time import strftime, gmtime

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
        
        self._startDate = message_data.get('startDate', None)
        self._criticality = message_data.get('criticality', None)
        self._resourceId = message_data.get('resourceId', None)
        self._alertId = message_data.get('alertId', None)
        self._status = message_data.get('status', None)
        self._subType = message_data.get('subType', None)
        self._cancelDate = message_data.get('cancelDate', None)
        self._resourceKind = message_data.get('resourceKind', None)
        self._adapterKind = message_data.get('adapterKind', None)
        self._type = message_data.get('type', None)
        self._resourceName = message_data.get('resourceName', None)
        self._updateDate = message_data.get('updateDate', None)
        self._info = message_data.get('info', None)

        self.message = message_data


    def _read_json(self, message):
        return json.load(message)


    # TODO:
    def _read_xml(self, message):
        return False


    @property
    def as_dict(self):
        return self.message


    @property
    def as_json(self):
        return json.dumps(self.message)


    @property
    def startDate(self):
        s, ms = divmod(self._startDate, 1000)
        return strftime('%Y-%m-%d %H:%M:%S', gmtime(s))


    @property
    def info(self):
        return self._info


    @property
    def status(self):
        return self._status


    @property
    def resourceName(self):
        return self._resourceName
