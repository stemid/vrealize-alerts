# Also an example that simply logs data to the logging handler provided.
import json

class LoggingPlugin(object):
    plugin_name = 'LoggingPlugin'

    def __init__(self, config, logging, **kw):
        self.l = logging
        self.config = config
        request = kw['request']

        body = request.body
        try:
            jbody = json.load(body)
        except Exception as e:
            self.l.exception('Caught exception parsing json: {error}'.format(
                error=str(e)
            ))

        self.message = jbody


    def run(self):
        l = self.l
        l.info('Alert: {data}'.format(
            data=json.dumps(self.message)
        ))
