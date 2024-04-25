from setuptools import setup, find_packages

setup(
    name='websocket-server-lib',
    author='Rohan Julka',
    description='Library for websocket support in Python',
    version='0.1',
    packages=find_packages(include=['ws', 'ws.*']),
    install_requires=[
        # Add any dependencies here
    ],
)