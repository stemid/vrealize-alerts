# Proxy API for vRealize REST alerts

vRealize is a system from VMware that can be configured to send alerts to a REST API with either JSON or XML data.

See more [here](https://pubs.vmware.com/vrealizeoperationsmanager-6/index.jsp?topic=%2Fcom.vmware.vcom.core.doc%2FGUID-2A26A734-CD91-43E0-BF42-B079D5B0F5D4.html). 

This simple Bottle based Python REST API proxies the alerts to another service of your choice. 

For the time being it only supports JSON callbacks from vRealize. No plans to implement XML right now but it is possible. 

# Service modules

To proxy the alert to a service a module is required, as of writing only Monitorscout is supported.

# Install

Disable plugins in plugins.cfg by commenting out their line.

## Plugins

Plugins must be installed into path to be discovered.

	$ python setup.py install

# Run server

	$ python app.py
