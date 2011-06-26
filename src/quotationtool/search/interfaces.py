import zope.interface
from zope.i18nmessageid import MessageFactory
from zope.viewlet.interfaces import IViewletManager
from z3c.searcher.interfaces import ISearchFilter


_ = MessageFactory('quotationtool')


class IQuotationtoolSearchFilter(ISearchFilter):
    """ Default search filter. Searches for any content."""


class ITypeExtent(zope.interface.Interface):

    def delimit():
        """ Limits the search to a type extension."""


class ISearchFilterProvider(zope.interface.Interface):

    filterFactory = zope.interface.Attribute(""" Factory to make search filter.""")

    resultURL = zope.interface.Attribute("""Search Result URL""")

    label = zope.interface.Attribute("""Label in UI""")

    session_name = zope.interface.Attribute("""Name of the filter in the session.""")

    
class ISearchResultPage(zope.interface.Interface):
    """ A marker interface for pages that show search results. The
    Search nav item is active on them."""


class ISearchResultInfo(IViewletManager):
    """ Information about search result."""



class ISearchFormPrimer(IViewletManager):
    """A viewlet manager for a primer to the search form. Register
    viewlets for snippets that should be displayed prior to the search
    form."""


class IQuery(zope.interface.Interface):
    """A query to a single catalog index."""


    conjunction = zope.schema.Choice(
        title = _('iquery-conjunction-title',
                  u"Conjunction"),
        description = _('iquery-conjunction-desc',
                        u"and / or"),
        required = True,
        vocabulary = 'quotationtool.search.query.conjunction',
        default = 'AND',
        )

    quality = zope.schema.Choice(
        title = _('iquery-quality-title',
                  u"Quality"),
        description = _('iquery-quality-desc',
                        u"(yes) / not; Position or Negation"),
        required = True,
        vocabulary = 'quotationtool.search.query.quality',
        default = 'YES',
        )

    catalog = zope.interface.Attribute("""The catalog that is queried.""")

    index = zope.schema.TextLine(
        title = _('iquery-index-title',
                  u"Index"),
        description = _('iquery-index-desc',
                        u"The name of the index to be searched."),
        required = True,
        )                  

##     query = zope.schema.TextLine(
##         title = _('iquery-query-title',
##                   u"Query"),
##         description = _('iquery-query-desc',
##                         u"The term to search for."),
##         required = True,
##         )

    query = zope.interface.Attribute("""The query value.""")

    @zope.interface.invariant
    def assertQueryValue(inst):
        """Assert that query type matches index type. """
        cat = inst.catalog
        idx = inst.catalog[inst.index]
        if idx.interface is not None:
            idx.interface[idx.field_name].validate(inst.query)
        else:
            pass
                                       

class IMultiIndexQuery(zope.interface.Interface):


    target = zope.schema.Choice(
        title = _('imultiindexquery-catalog-title',
                  u"Target"),
        description = _('imultiindexquery-catalog-desc',
                        u"What are you searching for?"),
        required = True,
        vocabulary = 'quotationtool.catalog.query.catalog',
        )

    queries = zope.schema.List(
        title = _('imultiindexquery-queries-title',
                  u"Queries"),
        description = _('imultiindexquery-queries-desc',
                        u"A List of query objects."),
        value_type = zope.schema.Object(title = _('imultiindexquery-queries-object-title',
                                                  u"Query"),
                                        schema = IQuery,
                                        required = True,
                                        ),
        required = False,
        )


class SearchTargetUtility(zope.interface.Interface):

    label = zope.interface.Attribute("""Label""")

    description = zope.interface.Attribute("""Description""")

    search_form = zope.interface.Attribute("""URL of search form.""")

    catalog_registration_name = zope.interface.Attribute("""Name the catalog is registered.""")

    
