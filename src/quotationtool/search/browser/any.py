import zope.schema
from z3c.indexer.search import SearchQuery
from z3c.indexer.query import TextQuery
from z3c.formui import form as pageletform
from z3c.form import field, button

from quotationtool.search.interfaces import _


any_fulltext = zope.schema.TextLine(
    title = _('any-fulltext-title', u"Free Text"),
    required = False,
    )
any_fulltext.__name__ = 'any_fulltext'


class AnySearchPagelet(pageletform.Form):

    fields = field.Fields(any_fulltext)
    
    ignoreContext = True

    prefix = 'searchanyfield.'

    action = u'/quotationtool/examples/@@searchResult.html'

    @button.buttonAndHandler(_(u"Search"), name='search')
    def handleSearch(self, action):
        data, errors = self.extractData()
        if data[any_fulltext.__name__]:
            raise Exception
