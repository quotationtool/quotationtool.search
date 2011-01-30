import zope.interface
from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory, IVocabulary


def conjunctions(*terms):
    return vocabulary.SimpleVocabulary.fromValues(
        ['AND', 'OR'])
zope.interface.alsoProvides(conjunctions, IVocabularyFactory)


def qualities(*terms):
    return vocabulary.SimpleVocabulary.fromValues(
        ['YES', 'NOT'])
zope.interface.alsoProvides(qualities, IVocabularyFactory)

