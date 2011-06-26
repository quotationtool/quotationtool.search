from zope.viewlet.manager import ViewletManager, WeightOrderedViewletManager
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.viewlet.viewlet import ViewletBase
from z3c.searcher.interfaces import ISearchSession

from quotationtool.search.interfaces import ISearchResultInfo


SearchResultInfo = ViewletManager('searchresultinfo', 
                                  ISearchResultInfo,
                                  bases = (WeightOrderedViewletManager,))


class ResultCountViewlet(ViewletBase):

    template = ViewPageTemplateFile('resultcount.pt')

    @property
    def filter_name(self):
        return getattr(self.__parent__, 'session_name', u'last')

    def render(self):
        return self.template()

    def count(self):
        session = ISearchSession(self.request)
        fltr = session.getFilter(self.filter_name)
        query = fltr.generateQuery()
        return len(query.searchResults())
