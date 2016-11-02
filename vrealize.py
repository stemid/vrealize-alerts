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
        # TODO: Go on...


    def read_json(self, message):
        return json.load(message)
