from setuptools import setup, find_packages
setup(
    name='mal-helper',
    version='1.0.0',
    description='A Python library to fetch data from MyAnimeList',
    author='Dominik Procházka',
    packages=find_packages(),
    install_requires=['flask', 'gevent', 'requests']
)