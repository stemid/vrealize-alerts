# Proxy API for vRealize REST alerts

import json
import pkg_resources
from uuid import UUID
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

from bottle import Bottle
from bottle import request, response, template, static_file

from logger import Logger
from vrealize import VRealizeAlert


# Custom UUID route filter for bottle.py
def uuid_filter(config):
    # Should catch UUIDv4 type strings
    regexp = r'[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}'

    def to_python(match):
        return UUID(match, version=4)

    def to_url(uuid):
        return str(uuid)

    return regexp, to_python, to_url


# Read configuration
config = RawConfigParser()
config.readfp(open('./api.cfg'))
config.read(['api_local.cfg', '/etc/vrealize-alerts/api.cfg'])

# Setup logging, and a shorthand for future log messages
log = Logger(config)

app = Bottle()
app.router.add_filter('uuid', uuid_filter)

# Set a json content type for all responses
@app.hook('after_request')
def json_response():
    response.content_type = 'application/json'


@app.route('/test', method=['POST', 'PUT'])
@app.route('/<alertid:uuid>', method=['POST', 'PUT'])
def index(alertid=None):
    log.debug('Received alert from {client_ip}: {data}'.format(
        client_ip=request.remote_route[0],
        data=str(request.body)
    ))

    # Most likely test alert
    if not alertid:
        return json.dumps({
            'status': True
        })

    # Process alert data
    try:
        alert = VRealizeAlert(request.body, content_type=request.content_type)
    except Exception as e:
        log.info(request.content_type)
        log.exception('Failed to load vrealize alert data: {error}'.format(
            error=str(e)
        ))
        raise

    # Launch plugins
    for entrypoint in pkg_resources.iter_entry_points('api.plugins'):
        log.debug('Loading plugin "{plugin}"'.format(
            plugin=entrypoint.name
        ))

        # Get plugin class and name from entrypoint
        plugin_class = entrypoint.load()
        plugin_name = entrypoint.name

        # Instantiate the plugin class
        try:
            inst = plugin_class(
                config,
                log,
                alert=alert
            )
        except Exception as e:
            log.exception('Exception while loading "{plugin}": {error}'.format(
                plugin=plugin_name,
                error=str(e)
            ))
            continue

        # Run plugin
        try:
            inst.run()
        except Exception as e:
            log.exception('Exception while running "{plugin}": {error}'.format(
                plugin=plugin_name,
                error=str(e)
            ))
            continue

    return json.dumps({
        'status': True
    })


if __name__ == '__main__':
    app.run(
        host=config.get('api', 'listen_host'),
        port=config.getint('api', 'listen_port')
    )
    debug(config.getbool('api', 'debug'))
else:
    application = app
