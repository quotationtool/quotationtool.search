import zope.interface
from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

import interfaces


class Query(object):
    """A query on an index.

        >>> import zope.interface
        >>> import zope.schema
        >>> class IPerson(zope.interface.Interface):
        ...     name = zope.schema.TextLine(title = u"Name")
        ...     born = zope.schema.Int(title = u"Year of Birth")

        >>> query = Query()
        >>> query.conjunction = 'AND'
        >>> query.quality = 'NOT'
        >>> from quotationtool.search.interfaces import IQuery
        >>> #query.index = IQuery['index']
        >>> query.index = u"born"
        >>> query.query = u"Help me, please, please, help me!"
        >>> IQuery.validateInvariants(query)
        Traceback (most recent call last):
        ...
        AttributeError: 'Query' object has no attribute 'catalog'

        >>> import zc.catalog
        >>> def testFilter(extent, uid, obj):
        ...     assert zc.catalog.interfaces.IFilterExtent.providedBy(extent)
        ...     return True

        >>> from zc.catalog.extentcatalog import FilterExtent, Catalog
        >>> extent = FilterExtent(testFilter)
        >>> cat = Catalog(extent)
        >>> from zope.catalog.text import TextIndex
        >>> cat['name'] = TextIndex(
        ...     interface = IPerson,
        ...     field_name = 'name',)

        >>> from zc.catalog.catalogindex import ValueIndex
        >>> cat['born'] = ValueIndex(
        ...     interface = IPerson,
        ...     field_name = 'born',
        ...     )

        >>> query.catalog = cat
        >>> IQuery.validateInvariants(query)
        Traceback (most recent call last):
        ...
        WrongType: (...)

        >>> query.index = u"name"
        >>> IQuery.validateInvariants(query)

        >>> query.index = u"born"
        >>> query.query = 1975
        >>> IQuery.validateInvariants(query)
        >>> 

    """

    zope.interface.implements(interfaces.IQuery)

    conjunction = FieldProperty(interfaces.IQuery['conjunction'])
    quality = FieldProperty(interfaces.IQuery['quality'])
    index = FieldProperty(interfaces.IQuery['index'])
    #query = FieldProperty(interfaces.IQuery['query'])


class PersistentQuery(Query, Persistent):
    """A query, but persistently stored in the ZODB. """


class MultiIndexQuery(object):
    """


    """

    zope.interface.implements(interfaces.IMultiIndexQuery)

    queries = FieldProperty(interfaces.IMultiIndexQuery['queries'])


class PersistentMultiIndexQuery(MultiIndexQuery, Persistent):
    """A query over multiple indexes, but persistently stored in ZODB."""
