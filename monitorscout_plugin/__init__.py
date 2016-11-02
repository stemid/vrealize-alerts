import json
import requests

class MonitorscoutPlugin(object):
    plugin_name = 'MonitorscoutPlugin'

    def __init__(self, config, logging, **kw):
        self.l = logging
        self.config = config
        alert = kw.get('alert')

        self.headers = {
            'X-Auth-API-Key': config.get(self.plugin_name, 'api_key'),
            'X-Requested-With': 'vRealize Alerts API',
            'Content-Type': 'application/json',
        }

        self.create_url = '{url}/{device}/create_alert'.format(
            url=config.get(self.plugin_name, 'api_url'),
            device=config.get(self.plugin_name, 'device_id')
        )

        alert_name = '{resourceName} {status}'.format(
            resourceName=alert.resourceName,
            status=alert.status
        )

        alert_msg = '{startDate}: \n{info}'.format(
            startDate=alert.startDate,
            info=alert.info
        )

        self.alert_data = {
            'name': alert_name,
            'error_msg': alert_msg
        }


    def run(self):
        config = self.config
        log = self.l

        r = self.device_alert()

        if r.status_code == 200:
            log.info('Created device alert successfully')
        else:
            log.debug('Error from MS API: {text}'.format(
                text=r.text
            ))


    def device_alert(self):
        return requests.put(
            self.create_url,
            headers=self.headers,
            data=json.dumps(self.alert_data)
        )
