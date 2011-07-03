import zope.component
from z3c.searcher.filter import SearchFilter
from z3c.searcher.interfaces import ISearchSession, ISearchCriterium, ISearchFilter
from z3c.pagelet.browser import BrowserPagelet
from zope.index.text import parsetree

from quotationtool.search.interfaces import _
from quotationtool.search.interfaces import ITypeExtent, ICriteriaChainSpecifier, IResultSpecifier
from quotationtool.search.interfaces import ICriteriumDescription
from quotationtool.search.searcher import QuotationtoolSearchFilter


class SearchForm(BrowserPagelet):
    """ A search form."""

    filterFactory = QuotationtoolSearchFilter

    label = _('search-form-label', u"Search")

    prefix = 'search.'

    status = []

    session_name = 'last'

    nonui_criteria = ('type-field',) # criteria non present on the UI

    @property
    def action(self):
        return self.request.getURL()

    @property
    def query(self):
        for factory in self.getCriteriaInOrder():
            if not factory[0] in self.nonui_criteria:
                yield factory[0]

    @property
    def criteria(self):
        for factory in self.getCriteriaInOrder():
            if not factory[0] in self.nonui_criteria:
                yield factory[1]()

    def getCriteriaInOrder(self):
        factories = self.filterFactory().criteriumFactories
        def getWeight(factory):
            try:
                desc = ICriteriumDescription(factory[1]())
            except Exception:
                desc = None
            return getattr(desc, 'ui_weight', ICriteriumDescription['ui_weight'].default)
        return sorted(factories, cmp=lambda x,y: cmp(getWeight(x), getWeight(y)))

    @property
    def filters(self):
        default = None
        for key, fltr in zope.component.getFactoriesFor(ISearchFilter):
            if not isinstance(fltr(), self.filterFactory):
                yield key, fltr
            else:
                default = (key, fltr)
        if default:
            yield default

    def getLabelsAndDescriptions(self):
        for name, factory in self.getCriteriaInOrder():
            crit = factory()
            try:
                desc = getattr(ICriteriumDescription(factory), 'description', u"")
            except Exception:
                desc = None
            crit_type = u""
            if ITextCriterium.providedBy(crit):
                crit_type = _(u"Fulltext Index") 
            yield (name, crit, desc, crit_type)
        
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
