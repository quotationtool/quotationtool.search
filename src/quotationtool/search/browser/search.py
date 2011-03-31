import zope.interface
import zope.component
from z3c.pagelet.browser import BrowserPagelet
from zope.catalog.interfaces import ICatalog
from zope.exceptions.interfaces import UserError
from zope.intid.interfaces import IIntIds
from zope.traversing.browser import absoluteURL
from zope.catalog.text import ITextIndex
from zope.viewlet import viewlet
from zope.viewlet.interfaces import IViewletManager
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
import zope.traversing
from zope.app.component import hooks
from zope.publisher.browser import BrowserView
from zope.i18nmessageid import MessageFactory
from zope.viewlet.manager import ViewletManager 

from quotationtool.search import interfaces
from quotationtool.search.interfaces import _


PREFIX = u'search.'


SearchFormPrimer = ViewletManager('search_form_primer',
                                  interfaces.ISearchFormPrimer,
                                  bases = (WeightOrderedViewletManager,))


class SearchFormBase(BrowserPagelet):
    """A base class form search forms."""
    
    catalog_name = 'NOT_IMPLEMENTED'

    prefix = PREFIX

    def getAction(self):
        """Override action or getAction for other urls."""
        return absoluteURL(self.context, self.request) + u"/@@searchResultPage.html"
    action = property(getAction)

    def getIndices(self):
        cat = zope.component.getUtility(
            ICatalog,
            name = self.catalog_name,
            context = self.context)
        for index in cat.values():
            # TODO: we can only query text indices, would have to add
            # more logic for value indeices in result page
            if ITextIndex.providedBy(index):
                yield index
        

class QuickSearchViewlet(viewlet.ViewletBase):
    """A viewlet for fast searching the quid_pro_quo index."""

    template = ViewPageTemplateFile('search_quick.pt')

    prefix = PREFIX

    container_utility = object # override!

    resultView = u"@@searchResultPage.html"

    index = 'NOT_DEFINED'

    query = ()

    full_fledged_url = u"/@@search.html"

    def render(self):
        return self.template()

    def __init__(self, context, request, view, manager):
        # use hooks because component lookup error if error is context
        site = hooks.getSite()
        iface = zope.component.getUtility(
            zope.interface.interfaces.IInterface, self.container_utility,
            context = site)
        container = zope.component.getUtility(
            iface, context = site)
        self.actionURL = absoluteURL(container, request) + u"/" + self.resultView
        self.fullFledgedURL = absoluteURL(site, request) + self.full_fledged_url
        super(QuickSearchViewlet, self).__init__(context, request, view, manager)


class SearchResultPageBase(BrowserPagelet):
    """A base class for search result in a page manner (N by page)."""

    catalog_name = 'NOT_IMPLEMENTED'

    prefix = PREFIX

    show_N = 50

    def update(self):
        cat = zope.component.getUtility(
            ICatalog,
            name = self.catalog_name,
            context = self.context)
        i = 0
        present = True
        self.query = {}
        while present:
            if self.request.form.has_key(self.prefix + str(i) + u".index"):
                index = self.request.form.get(self.prefix + str(i) + u".index")
                query = self.request.form.get(self.prefix + str(i) + u".query")
                # ignore empty query fields
                if query not in (u"", None):
                    self.query[str(index)] = query
                i += 1
            else:
                present = False
        for idx, query in self.query.items():
            # assert indices from the catalog
            if idx not in cat.keys():
                raise UserError(_('search-invalid-index-error',
                                  u"Index ${index} not found!",
                                  mapping = {'index':idx}))
            # assert query matches index type
            try:
                cat[idx].interface[idx].validate(query)
            except Exception, err:
                raise UserError(_('search-query-type-error',
                                  u"Invalid query for ${index}",
                                  mapping = {'index': idx})
                                + unicode(err)) 
        if len(self.query) > 0:
##             try:
##                 self.result = cat.apply(self.query)
##             except Exception, err:
##                 raise UserError(err)
            self.result = cat.apply(self.query)
        else:
            self.result = []

    def getResultPage(self):
        #raise Exception(self.result)
        intid_ut = zope.component.getUtility(
            IIntIds, context = self.context)
        for i in self.result:
            yield intid_ut.getObject(i)


class ISearchTargetManager(IViewletManager):
    """A manager for viewlets that lets a user choose a database to
    search, i.e. a target to search for.

    The policy of the quotationtool app is that there are searchforms
    for each type of target. The user has to choose the target
    first. The target options are presented with this viewlet
    manager. Instantiation of a viewlet is done via zcml..."""


class SearchTargetManager(WeightOrderedViewletManager):
    zope.interface.implements(ISearchTargetManager)


INPUT_NAME = 'url'

    
class SearchTargetViewlet(viewlet.ViewletBase):
    """A viewlet class for a search target option."""

    template = ViewPageTemplateFile('search_target.pt')

    input_name = INPUT_NAME

    searchFormURL = u"set from zcml!"

    label = u"MESSAGE-ID (write subclass from this class!)"

    description = u"MESSAGE-ID (write subclass from this class!)"

    def render(self):
        return self.template()


class ChooseSearchTarget(BrowserPagelet):
    """A view that lets the user choose a search target."""


class ChooseSearchTargetRedirector(BrowserView):
    """Redirects to the form for the choosen target"""

    def siteURL(self):
        return absoluteURL(hooks.getSite(), self.request)

    def __call__(self):
        view = self.request.form.get(INPUT_NAME, None)
        if view is None:
            raise UserError(_('choose-search-target',
                              u"Please choose a search target!"))
        self.request.response.redirect(self.siteURL() + u"/" + view)
        return
