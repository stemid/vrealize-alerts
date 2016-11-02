# Also an example that simply logs data to the logging handler provided.

class LoggingPlugin(object):
    plugin_name = 'LoggingPlugin'

    def __init__(self, config, logging, **kw):
        self.l = logging
        self.config = config
        self.alert = kw.get('alert')


    def run(self):
        l = self.l
        l.info('Alert: {data}'.format(
            data=self.alert.message_json
        ))
