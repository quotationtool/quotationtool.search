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
    #common.setUpConjunctionVocabulary(test)
    #common.setUpQualityVocabulary(test)


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocTestSuite('quotationtool.search.query',
                                 setUp = setUpZCML,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            ))
