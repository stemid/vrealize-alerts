# Proxy API for vRealize REST alerts

# Makes debugging easier
from pprint import pprint as pp

import json
import pkg_resources

# Until pyvenv-3.4 is fixed on centos 7 support python 2.
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

from bottle import default_app, route, run, hook
from bottle import request, response, template, static_file

from logger import Logger


# Read configuration
config = RawConfigParser()
config.readfp(open('./api.cfg'))
config.read(['api_local.cfg', '/etc/vrealize-alerts/api.cfg'])

# Setup logging, and a shorthand for future log messages
log = Logger(config)

# Set a json content type for all responses
@hook('after_request')
def json_response():
    response.content_type = 'application/json'


@route('/', method=['POST', 'PUT'])
def index():
    log.debug('Received alert from {client_ip}: {data}'.format(
        client_ip=request.remote_route[0],
        data=str(request.body)
    ))

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
                request=request
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
    run(
        host=config.get('api', 'listen_host'),
        port=config.getint('api', 'listen_port')
    )
    debug(config.getbool('api', 'debug'))
else:
    application = default_app()
