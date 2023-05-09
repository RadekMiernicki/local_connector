from setuptools import setup

setup(
    name='local_connector',
    version='0.1.1',
    description='Connector to MySQL on localhost',
    author='Radek Miernicki',
    author_email='radek.miernicki@gmail.com',
    packages=['local_connector'],  # same as name
    install_requires=['mysql.connector'], # external packages as dependencies
)

