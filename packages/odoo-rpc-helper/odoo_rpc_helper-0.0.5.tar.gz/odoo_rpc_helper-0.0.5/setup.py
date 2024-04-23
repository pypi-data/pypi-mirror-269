from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='odoo_rpc_helper',
    version='0.0.5',
    packages=find_packages(),
    author='Marc Durepos',
    author_email='marc@bemade.org',
    description='A simple wrapper for more easily running Odoo RPC commands.',
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='odoo rpc xmlrpc',
    url='https://github.com/bemade/odoo_rpc_helper',

)

