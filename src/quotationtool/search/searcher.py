import zope.interface
import zope.component
from z3c.searcher.filter import SearchFilter, EmptyTerm
from z3c.searcher.criterium import TextCriterium, SearchCriterium, factory
from z3c.searcher.interfaces import CONNECTOR_AND, CONNECTOR_OR
from zope.i18nmessageid import MessageFactory
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.traversing.api import getParents

from quotationtool.site.interfaces import IQuotationtoolSite

from quotationtool.search import interfaces
from quotationtool.search.interfaces import _


class QuotationtoolSearchFilter(SearchFilter):
    """ Search filter."""

    zope.interface.implements(interfaces.IQuotationtoolSearchFilter,
                              interfaces.ITypeExtent,
                              interfaces.ICriteriaChainSpecifier,
                              interfaces.IResultSpecifier)

    def getDefaultQuery(self):
        return EmptyTerm()

    def delimit(self):
        """ We don't have to do anything."""
        pass

    first_criterium_connector_name = CONNECTOR_OR

    ignore_empty_criteria = True

    def resultURL(self, context, request): 
        site = None 
        for path_element in [context]+getParents(context): 
            if IQuotationtoolSite.providedBy(path_element): 
                site = path_element 
                return absoluteURL(site, request) + u"/@@searchResult.html"

    session_name = 'any'


quotationtool_search_filter_factory = zope.component.factory.Factory(
    QuotationtoolSearchFilter,
    _('QuotationtoolSearchFilter-title', u"Any Content"),
    _('QuotationtoolSearchFilter-desc', u"Search for all content types.")
    )


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


class IdCriterium(SearchCriterium):
    """ Search criterium for 'id-field' index."""

    indexOrName = 'id-field'

    label = _('id-field-label', u"ID")

id_factory = factory(IdCriterium, 'id-field')    
