from setuptools import setup, find_packages

try:
    plugins = open('/etc/vrealize-alerts/plugins.cfg')
except:
    plugins = open('plugins.cfg')

setup(
    name="vRealizeAPIPlugins",
    version="0.1",
    description="vRealize Alerts REST API Plugins",
    author="Stefan Midjich",
    packages=find_packages(),
    entry_points=plugins.read()
)
