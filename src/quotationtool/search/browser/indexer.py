import zope.component
from z3c.pagelet.browser import BrowserPagelet
from z3c.indexer.indexer import index
from zope.intid.interfaces import IIntIds
from z3c.indexer.interfaces import IIndex

class IndexObjects(BrowserPagelet):

    count = 0

    def update(self):
        # clear indices
        for idx in zope.component.getAllUtilitiesRegisteredFor(IIndex, context=self.context):
            idx.clear()
        # index all registered objects
        super(IndexObjects, self).update()
        intids = zope.component.getUtility(
            IIntIds, context=self.context)
        for iid in intids:
            index(intids.getObject(iid))
            self.count += 1

    def render(self):
        return u"Indexed %d objects." % self.count
