from setuptools import setup, find_packages
setup(
    name='alfetcher',
    version='1.0.0a',
    description='A Python library to fetch data from Anilist',
    author='Dominik Procházka',
    packages=find_packages(),
    install_requires=['flask', 'gevent', 'requests']
)