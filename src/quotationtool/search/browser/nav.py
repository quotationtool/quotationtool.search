import zope.interface
import zope.component
from zope.viewlet.manager import ViewletManager
from z3c.menu.ready2go import ISiteMenu
from z3c.menu.ready2go.manager import MenuManager
from z3c.menu.ready2go.item import SiteMenuItem

from quotationtool.skin.interfaces import ISubNavManager
from quotationtool.skin.browser.nav import MainNavItem


class ISearchMainNavItem(zope.interface.Interface): 
    """ A marker interface for the bibliography's item in the main navigation."""
    pass


class SearchMainNavItem(MainNavItem):
    """The bibliography navigation item in the main navigation."""

    zope.interface.implements(ISearchMainNavItem)


class ISearchSubNav(ISubNavManager):
    """A manager for the bibliography subnavigation."""


SearchSubNav = ViewletManager('searchsubnav',
                              ISiteMenu,
                              bases = (MenuManager,))

ISearchSubNav.implementedBy(SearchSubNav)

