import unittest
import doctest
import zope.component
from zope.component.testing import setUp, tearDown, PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig 

import quotationtool.search


def setUpZCML(test):
    """
        >>> import quotationtool.search
        >>> from zope.configuration.xmlconfig import XMLConfig
        >>> XMLConfig('configure.zcml', quotationtool.search)()

    """
    XMLConfig('configure.zcml', quotationtool.search)()


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocFileSuite('README.txt',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            ))
