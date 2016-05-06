#!/usr/bin/env python
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
from setuptools import setup

config = configparser.ConfigParser()
config.read('setup.ini')

readme = open("README.md", "r")


setup(name='fjorton',
      version=config.get('setup', 'release'),
      description='Python Netlink library',
      author='Peter V. Saveliev',
      author_email='peter@svinota.eu',
      url='https://github.com/svinota/fjorton',
      license='dual license GPLv2+ and Apache v2',
      packages=['fjorton'],
      install_requires=['byteplay'],
      classifiers=['License :: OSI Approved :: GNU General Public ' +
                   'License v2 or later (GPLv2+)',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: ' +
                   'Python Modules',
                   'Operating System :: POSIX',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Development Status :: 4 - Beta'],
      long_description=readme.read())
