import zope.component
from z3c.pagelet.browser import BrowserPagelet
from z3c.indexer.indexer import index
from zope.intid.interfaces import IIntIds

class IndexObjects(BrowserPagelet):

    count = 0

    def update(self):
        super(IndexObjects, self).update()
        intids = zope.component.getUtility(
            IIntIds, context=self.context)
        for iid in intids:
            index(intids.getObject(iid))
            self.count += 1

    def render(self):
        return u"Indexed %d objects." % self.count
