__author__ = 'atrimble'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'BigIO',
    'author': 'Andrew Trimble',
    'url': 'www.bigio.io',
    'download_url': 'https://github.com/Archarithms/bigio',
    'author_email': 'andrew.trimble@archarithms.com',
    'version': '0.1',
    'install_requires': ['nose', 'msgpack-python', 'netifaces'],
    'packages': ['bigio'],
    'scripts': [],
    'name': 'bigio'
}
