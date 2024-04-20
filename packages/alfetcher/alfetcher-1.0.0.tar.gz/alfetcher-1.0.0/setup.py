from setuptools import setup, find_packages
setup(
    name='al-helper',
    version='1.0.0',
    description='A Python library to fetch data from Anilist',
    author='Dominik Procházka',
    packages=find_packages(),
    install_requires=['flask', 'gevent', 'requests']
)