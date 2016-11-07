import json
import requests
from xmlrpclib import ServerProxy

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

        self.close_url = '{url}/{device}/close_alert'.format(
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

        self.alert = alert

        # Connect to MS RPC API
        if config.has_option('MonitorscoutPlugin', 'rpc_api_url'):
            api_url = config.get('MonitorscoutPlugin', 'rpc_api_url')
            api_username = config.get('MonitorscoutPlugin', 'rpc_api_username')
            api_password = config.get('MonitorscoutPlugin', 'rpc_api_password')
            if config.has_option('MonitorscoutPlugin', 'rpc_api_account'):
                api_account = config.get('MonitorscoutPlugin', 'rpc_api_account')
            else:
                api_account = None

            self.ms = ServerProxy(api_url)
            self.ms_sid = self.ms.login(
                api_username,
                api_password,
                api_account
            )


    def run(self):
        config = self.config
        log = self.l

        # Close any ACTIVE device alerts that have been created with the
        # same resourceName in MS.
        if self.alert.status == 'CANCELED':
            try:
                self.close_device_alert()
            except Exception as e:
                log.exception('Exception while trying to close device alert')
                # Continue anyways because it might mean MS RPC API is
                # unconfigured.
                pass
        else:
            r = self.make_device_alert()

            if r.status_code == 200:
                log.info('Created device alert successfully')
            else:
                log.error('Error creating device alert: {text}'.format(
                    text=r.text
                ))


    def make_device_alert(self):
        return requests.put(
            self.create_url,
            headers=self.headers,
            data=json.dumps(self.alert_data)
        )


    def close_device_alert(self):
        device_alerts = self.ms.device.get_alerts(
            self.ms_sid,
            self.config.get('MonitorscoutPlugin', 'device_id')
        )

        for entity_id, entity in device_alerts.get('entity_data').items():
            if entity.get('type', '') != 'device_alert':
                continue

            log = self.l

            alert_name = '{resourceName} ACTIVE'.format(
                resourceName=self.alert.resourceName
            )

            alert_data = {
                'name': alert_name
            }

            if entity.get('name', '') == alert_name:
                res = requests.put(
                    self.close_url,
                    headers=self.headers,
                    data=json.dumps(alert_data)
                )

                if res.status_code == 200:
                    log.info('Closed device alert {id} successfully'.format(
                        id=entity.get('id', '')
                    ))
                else:
                    log.error('Error closing device alert {id}: {text}'.format(
                        id=entity.get('id', ''),
                        text=res.text
                    ))
