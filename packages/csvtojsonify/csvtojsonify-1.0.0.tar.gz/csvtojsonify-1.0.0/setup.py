# setup.py
from setuptools import setup

setup(
    name='csvtojsonify',
    version='1.0.0',
    packages=['csvtojsonify'],
    entry_points={
        'console_scripts': [
            'csvtojsonify = csvtojsonify:main',
        ],
    },
    author='Sriram Sreedhar',
    author_email='sriramsreedhar003@email.com',
    description='A tool to convert CSV to JSON',
)
