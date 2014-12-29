from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(
    name='ckanext-searchhistory',
    version=version,
    description="Store a search history and make it available for displaying",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Nigel Babu',
    author_email='nigel.babu@okfn.org',
    url='http://github.com/ckan/ckanext-searchhistory',
    license='AGPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.searchhistory'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        search_history=ckanext.searchhistory.plugin:SearchHistoryPlugin
    ''',
)
