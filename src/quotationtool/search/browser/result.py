import zope.interface
import zope.component
from z3c.pagelet.browser import BrowserPagelet
from z3c.searcher.interfaces import ISearchSession
from z3c.table.interfaces import ITable
from z3c.table import table, value, column
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.contentprovider.interfaces import IContentProvider
from zope.i18n import translate

from quotationtool.search.interfaces import _, ISearchResultPage


class ISearchResultTable(ITable):
    """ The table for search result."""


class SearchResult(table.SequenceTable, BrowserPagelet):
    """ Display search results when any content is searched."""

    zope.interface.implements(ISearchResultTable,
                              ISearchResultPage)

    session_name = 'any'

    render = BrowserPagelet.render

    cssClasses = {
        'table': u'container-listing',
        'thead': u'head',
        }

    cssClassEven = u'even'
    cssClassOdd = u'odd'


class SearchResultValues(value.ValuesMixin):
    """ Values (any objects) from a search result."""

    zope.component.adapts(zope.interface.Interface,
                          IBrowserRequest, 
                          SearchResult)

    @property
    def values(self):
        session = ISearchSession(self.request)
        fltr = session.getFilter(self.table.session_name)
        query = fltr.generateQuery()
        for obj in query.searchResults():
            yield obj


class LabelColumn(column.LinkColumn):
    """ The quid attribute of an example object."""

    header = _('label-column', u"Item type")
    weight = 10

    def getLinkContent(self, item):
        label = zope.component.getMultiAdapter(
            (item, self.request), name='label').__call__()
        return translate(label)


class ListViewColumn(column.Column):
    """ The quid attribute of an example object."""

    header = _('listview-column', u"Item")
    weight = 20

    def renderCell(self, item):
        return zope.component.getMultiAdapter(
            (item, self.request), name='list').__call__()


class FlagsColumn(column.Column):
    """ The flags of a example."""

    header = _(u"flags")
    weight = 99999
    
    def renderCell(self, item):
        flags = zope.component.getMultiAdapter(
            (item, self.request, self.table),
            IContentProvider, name='flags')
        flags.update()
        return flags.render()
