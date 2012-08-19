import zope.interface
import zope.schema
from zope.i18nmessageid import MessageFactory
from zope.viewlet.interfaces import IViewletManager
from z3c.searcher.interfaces import ISearchFilter, connectorVocabulary, CONNECTOR_OR


_ = MessageFactory('quotationtool')


class IQuotationtoolSearchFilter(ISearchFilter):
    """ Default search filter. Searches for any content."""


class ITypeExtent(zope.interface.Interface):
    """ Delimit search result to a specific content type (or any other
    extension)."""

    def delimit():
        """ Limits the search to a type extension."""


class ICriteriaChainSpecifier(zope.interface.Interface):
    """ Specifications on how to build the criteria chain on a search filter."""

    first_criterium_connector_name = zope.schema.Choice(
        title = u"First Criterium Connector Name",
        description = u"The name of the connector name on the first criterium. Note: First criterium means the first none-empty criterium if and only if 'Ignore Empty Criteria' is selected True.",
        vocabulary = connectorVocabulary,
        default = CONNECTOR_OR,
        required = True,
        )

    ignore_empty_criteria = zope.schema.Bool(
        title = u"Ignore Empty Criteria",
        description = u"Ignore empty search criteria (white space only) in the search form.",
        required = False,
        default = True,
        )


class ISearchFormExtension(IViewletManager):
    """ Viewlets may be registered for this manager."""


class ICriteriaReturningForm(zope.interface.Interface):
    """ May be implemented by search form extensions."""

    def getCriteria():
        """ Returns criteria."""


class IResultSpecifier(zope.interface.Interface):
    """ Provides Information about the search result page and provides
    this page with info."""

    def resultURL(context, request):
        """ Returns the URL of the result page. Requires context and
        request passed in."""

    session_name = zope.schema.ASCII(
        title = u"Filter",
        description = u"The name of the filter in the session.",
        required = True,
        default = 'any',
        )

class ICriteriumDescription(zope.interface.Interface):
    """ Provide the user with a description of the search
    criterium."""

    description = zope.schema.TextLine(
        title = u"Description",
        description = u"Provides the user with a description of the search criterium.",
        required = False,
        )

    ui_weight = zope.schema.Int(
        title = u"Weight",
        description = u"Defines the position of the criterium in the search form.",
        required = False,
        default = 9999,
        )

    
class ISearchResultPage(zope.interface.Interface):
    """ A marker interface for pages that show search results. The
    Search nav item is active on them."""


class ISearchResultInfo(IViewletManager):
    """ Information about search result."""

