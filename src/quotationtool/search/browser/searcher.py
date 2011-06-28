import zope.component
from z3c.searcher.filter import SearchFilter
from z3c.searcher.interfaces import ISearchSession, ISearchCriterium, ISearchFilter
from z3c.pagelet.browser import BrowserPagelet
from zope.index.text import parsetree

from quotationtool.search.interfaces import _
from quotationtool.search.interfaces import ITypeExtent, ICriteriaChainSpecifier, IResultSpecifier
from quotationtool.search.searcher import QuotationtoolSearchFilter


class SearchForm(BrowserPagelet):
    """ A search form."""

    filterFactory = QuotationtoolSearchFilter

    prefix = 'search.'

    status = []

    session_name = 'last'

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
        return zope.component.getFactoriesFor(ISearchFilter)
                
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

            fltr = zope.component.createObject(
                str(form.get(self.prefix+u"filter", 
                             u"quotationtool.search.searcher.QuotationtoolSearchFilter"))
                )
            if not fltr:
                fltr = self.filterFactory()

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
                if criteria_count == 0:
                    crit.connectorName = ICriteriaChainSpecifier(fltr).first_criterium_connector_name
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

            session.addFilter(IResultSpecifier(fltr).session_name, fltr)
            self.request.response.redirect(IResultSpecifier(fltr).resultURL(
                    self.context, self.request))
