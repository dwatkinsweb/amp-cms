#-------------------------------------------------------------------------------
# Copyright David Watkins 2011
# 
# AMP-CMS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

from content_type import BaseContentType
from ampcms.models import Module, Page
from ampcms.lib.pagelets import MenuPagelet

class MenuTypes:
    MAIN = 'menu-main'
    SIDE = 'menu-side'

class BaseLayout(BaseContentType):
    '''
    Base Layout object to extend when creating different layouts
    '''
    def __init__(self, page=None, *args, **kwargs):
        '''
        @param page: ampcms page object
        '''
        super(BaseLayout, self).__init__(*args, **kwargs)
        self._page = page
        self._template = 'layout.html'

    def _build_children(self):
        '''
        Build the children for the layout based on the users permissions
        '''
        if self._page:
            children = {'page' : self._page}
            children.update(self._build_menus())
        else:
            children = {}
        return children

    def _build_menus(self):
        '''
        Build the main and sub menus for the application based on modules and pages
        '''
        menus = {}
        # Build main menu
        menus[MenuTypes.MAIN] = MenuPagelet(menu_label=MenuTypes.MAIN, selected_item=self._page._data_model.module.title,
                                            request=self.request, request_kwargs=self.request_kwargs)
        for module in Module.objects.active_user_site_modules(self.request.user, self._page._data_model.module.site):
            menus[MenuTypes.MAIN].append(module.title, '/%s' % module.name)
        # Build side menu
        menus[MenuTypes.SIDE] = MenuPagelet(MenuTypes.SIDE, self._page._data_model.title,
                                            request=self.request, request_kwargs=self.request_kwargs)
        for page in Page.objects.active_user_site_pages(self.request.user, self._page._data_model.module.site, module=self._page._data_model.module):
            menus[MenuTypes.SIDE].append(page.title, '/%s/%s' % (page.module.name, page.name))
        return menus

class PCLayout(BaseLayout):
    pass
