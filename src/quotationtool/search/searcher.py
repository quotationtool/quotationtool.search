import zope.interface
from z3c.searcher.filter import SearchFilter, EmptyTerm
from z3c.searcher.criterium import TextCriterium, SearchCriterium, factory
from z3c.searcher.interfaces import CONNECTOR_AND
from zope.i18nmessageid import MessageFactory

from quotationtool.search.interfaces import _, IQuotationtoolSearchFilter, ITypeExtent


class QuotationtoolSearchFilter(SearchFilter):
    """ Search filter."""

    zope.interface.implements(IQuotationtoolSearchFilter,
                              ITypeExtent)

    def getDefaultQuery(self):
        return EmptyTerm()

    def delimit(self):
        """ We don't have to do anything."""
        pass
        

class AnyCriterium(TextCriterium):
    """ Full text criterium for 'any-fulltext' index."""

    indexOrName = 'any-fulltext'

    label = _('any-fulltext-label', u"Free Text (Any Field)")

any_factory = factory(AnyCriterium, 'any-fulltext')


class TypeCriterium(SearchCriterium):
    """ Search criterium for 'type-field' field index.

    Because we use this to limit the extent of a search result to a
    certain content type, this criterium 'and'-connects. """

    indexOrName = 'type-field'

    label = _('type-field-label', u"Search Target")

    connectorName = CONNECTOR_AND

type_factory = factory(TypeCriterium, 'type-field')
