import subprocess
from setuptools import setup, find_packages, Extension

setup(
    name = 'PGDecoy',
    version = '1.0.0',
    author = 'Chris Ellis',
    license = 'Postgresql',
    packages = [ 'PGDecoy' ],
    install_requires = [
        'httplib2'
    ]
)
