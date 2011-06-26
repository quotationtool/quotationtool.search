import zope.component
from quotationtool.site.interfaces import INewQuotationtoolSiteEvent
from z3c.indexer.interfaces import IIndex
from z3c.indexer.index import TextIndex, FieldIndex


def createIndices(site):
    """ Create indexes that are relevant for the site."""

    sm = site.getSiteManager()
    default = sm['default']

    if not default.has_key('any-fulltext'):
        any_fulltext = default['any-fulltext'] = TextIndex()
        sm.registerUtility(any_fulltext, IIndex, name='any-fulltext')

    if not default.has_key('type-field'):
        type_field = default['type-field'] = FieldIndex()
        sm.registerUtility(type_field, IIndex, name='type-field')


@zope.component.adapter(INewQuotationtoolSiteEvent)
def createIndicesSubscriber(event):
    """ Create indices when site is created."""

    createIndices(event.object)
