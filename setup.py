# -*- coding: utf-8 -*-
"""Setup for quotationtool.search package

$Id$
"""
from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

name='quotationtool.search'

setup(
    name = name,
    version='0.1.0',
    description="Search related components for the quotationtool application",
    long_description=(
        read('README')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('src', 'quotationtool', 'search', 'README.txt')
        + '\n' +
        'Download\n'
        '********\n'
        ),
    keywords='quotationtool, blue bream',
    author=u"Christian Luck",
    author_email='cluecksbox@googlemail.com',
    url='',
    license='ZPL 2.1',
    # Get more from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Programming Language :: Python',
                 'Environment :: Web Environment',
                 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                 'Framework :: Zope3',
                 ],
    packages = find_packages('src'),
    namespace_packages = ['quotationtool',],
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        'setuptools',
        'zope.interface',
        'zope.component',
        'zope.schema',
        'zope.app.schema',
        'zope.security',
        'zope.securitypolicy',
        'z3c.indexer',
        'z3c.searcher',

        # for browser related components
        'zope.exceptions',
        'zope.intid',
        'zope.traversing',
        'zope.viewlet',
        'zope.app.pagetemplate',
        'zope.app.component',
        'zope.publisher',
        'zope.i18nmessageid',
        'z3c.pagelet',
        'z3c.template',
        'z3c.macro',
        'zope.browserpage',
        'zope.publisher',
        'z3c.form',
        'zope.app.publisher',
        'z3c.menu.ready2go',
        'z3c.layer.pagelet',
        'z3c.formui',

        'quotationtool.skin',
        'quotationtool.site',
        'quotationtool.security',
        ],
    extras_require = dict(
        test = [
            'zope.testing',
            'zope.configuration',
            ],
        ),
    )
