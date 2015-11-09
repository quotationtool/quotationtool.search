import zope.component
from z3c.searcher.filter import SearchFilter
from z3c.searcher.interfaces import ISearchSession, ISearchCriterium, ISearchFilter
from z3c.pagelet.browser import BrowserPagelet
from zope.index.text import parsetree
from zope.viewlet.manager import ViewletManager, WeightOrderedViewletManager
from zope.contentprovider.interfaces import IContentProvider
from zope.viewlet.interfaces import IViewletManager
from z3c.template.interfaces import IContentTemplate
from zope.viewlet.viewlet import ViewletBase

from quotationtool.search.interfaces import _
from quotationtool.search import interfaces
from quotationtool.search.interfaces import ITypeExtent, ICriteriaChainSpecifier, IResultSpecifier
from quotationtool.search.interfaces import ICriteriumDescription
from quotationtool.search.searcher import QuotationtoolSearchFilter


class SearchFormMixin(object):
    """ A mixin class for search forms."""

    filterFactory = QuotationtoolSearchFilter

    label = _('search-form-label', u"Search")

    prefix = 'search.'

    status = []

    session_name = 'last'

    nonui_criteria = ('type-field',) # criteria non present on the UI

    options_info = True

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
        
    def _updateForm(self):
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

            # get criteria from search form extensions
            extensions = zope.component.getMultiAdapter(
                (self.context, self.request, self),
                interfaces.ISearchFormExtension,
                name = 'searchform-extension')
            extensions.update()
            extended_criteria = []
            for extension in extensions.viewlets:
                if interfaces.ICriteriaReturningForm.providedBy(extension):
                    extended_criteria += extension.getCriteria(fltr, criteria_count, self.status)
            for crit in extended_criteria:
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


class SearchForm(BrowserPagelet, SearchFormMixin):
    """ A search form."""

    def update(self):
        super(SearchForm, self).update()
        self._updateForm()


class SearchViewlet(ViewletBase, SearchFormMixin):
    """A search form in a viewlet.  It presents exactly the same search
    form as the SearchForm pagelet.

    """

    template = None

    def update(self):
        self._updateForm()

    def render(self):
        if self.template is None:
            template = zope.component.getMultiAdapter(
                (self, self.request), IContentTemplate)
            return template(self)
        return self.template()


class SimpleSearchViewlet(SearchViewlet):
    """ A viewlet presenting a simple search form with only one search criterium."""

    options_info = False

    @property
    def query(self):
        """ Yield only one criterium."""
        for factory in self.getCriteriaInOrder():
            if not factory[0] in self.nonui_criteria:
                yield factory[0]
                break



SearchFormExtensionManager = ViewletManager('searchform-extension',
                                            interfaces.ISearchFormExtension,
                                            bases=(WeightOrderedViewletManager,))
