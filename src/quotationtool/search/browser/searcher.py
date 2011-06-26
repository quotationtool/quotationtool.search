import zope.component
import zope.interface
from z3c.searcher.filter import SearchFilter
from z3c.searcher.interfaces import ISearchSession, ISearchCriterium
from zope.traversing.browser import absoluteURL
from z3c.pagelet.browser import BrowserPagelet
from zope.index.text import parsetree
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.component.hooks import getSite

from quotationtool.search.interfaces import ISearchFilterProvider, _
from quotationtool.search.interfaces import ITypeExtent
from quotationtool.search.searcher import QuotationtoolSearchFilter


class DefaultSearchFilterProvider(object):
    """ Provide search for with search filter and information about it."""
    
    zope.interface.implements(ISearchFilterProvider)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    filterFactory = QuotationtoolSearchFilter

    label = _('quotationtoolsearchfilterprovider-label', u"Any Content")

    type_query = u''

    session_name = 'any'

    @property
    def resultURL(self):
        site = getSite()
        return absoluteURL(site, self.request) + u"/@@searchResult.html"


class SearchForm(BrowserPagelet):
    """ A search form."""

    filterFactory = QuotationtoolSearchFilter

    prefix = 'search.'

    status = []

    session_name = 'last'

    or_connector_on_first_criterium = True
    
    @property
    def action(self):
        return self.request.getURL()

    @property
    def query(self):
        yield 'any-fulltext'
        for factory in self.filterFactory().criteriumFactories:
            if factory[0] == 'any-fulltext': continue
            if factory[0] == 'type-field': continue
            yield factory[0]

    @property
    def filters(self):
        return zope.component.getAdapters(
            (self.context, self.request, self),
            ISearchFilterProvider)
                
    def getCriteria(self):
        for factory in self.filterFactory().criteriumFactories:
            if factory[0] == 'type-field': continue
            yield factory[1]()
        
    def update(self):
        super(SearchForm, self).update()
        form = self.request.form
        criteria_count = 0
        self.status = []
        if form.get(self.prefix+'button.search', u"") == 'search':

            filterProvider = zope.component.getMultiAdapter(
                (self.context, self.request, self),
                interface=ISearchFilterProvider,
                name=form.get(str(self.prefix+u"filter"), 'default'))
            if not filterProvider:
                fltr = self.filterFactory()
            else:
                fltr = filterProvider.filterFactory()

            for i in range(len(list(self.query))):
                connector = form.get(self.prefix+unicode(i)+u'.connector', u"OR")
                criterium = form.get(self.prefix+unicode(i)+u'.criterium', u"")
                query = form.get(self.prefix+unicode(i)+u'.query', u"")
                if not (criterium and query):
                    continue
                try:
                    crit = fltr.createCriterium(criterium)
                except Exception, err:
                    self.status.append(_("Bad criterium '$CRITERIUM'.",
                                    mapping = {'CRITERIUM': criterium}))
                    continue
                #try:
                #    ISearchCreterium['connectorName'].validate(connector)
                #except Exception:
                #    self.status.append(_("Bad connector '$CONNECTOR'.",
                #                    mapping = {'CONNECTOR': connector}))
                #    return
                crit.value = query
                if criteria_count == 0 and self.or_connector_on_first_criterium:
                    # help users who do not think about it
                    crit.connectorName = 'OR'
                else:
                    crit.connectorName = connector
                fltr.addCriterium(crit)
                criteria_count += 1

            # no input 
            if not criteria_count:
                self.status.append(_(u"No values provided."))
                return

            # limit to filter target using type-field index or what ever
            ITypeExtent(fltr).delimit()

            try:
                query = fltr.generateQuery()
                result = query.searchResults()
            except TypeError:
                self.status.append(_('One of the search filters is setup improperly.'))
                # Return an empty result, since an error must have occurred
                return
            except parsetree.ParseError, error:
                self.status.append(_('Invalid search text.'))
                return
            self.status.append(u"Found %d objects" % len(result))
            session = ISearchSession(self.request)
            session.addFilter(self.session_name, fltr)

            if filterProvider:
                session.addFilter(filterProvider.session_name, fltr)
                self.request.response.redirect(filterProvider.resultURL)
