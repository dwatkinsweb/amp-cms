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

from base import BaseContentType
from ampcms.models import Module, Page
from ampcms.lib.content_type.pagelets import MenuPagelet

from django.conf import settings


class MenuTypes:
    MAIN = 'menu-main'
    SIDE = 'menu-side'


class BaseLayout(BaseContentType):
    """
    Base Layout object to extend when creating different layouts
    """

    def __init__(self, page=None, *args, **kwargs):
        """
        @param page: ampcms page object
        """
        super(BaseLayout, self).__init__(*args, **kwargs)
        self._page = page
        self._template = 'layout.html'

    def _get_context(self):
        context = super(BaseLayout, self)._get_context()
        context['base_template'] = settings.AMPCMS_BASE_TEMPLATE
        return context

    def _build_children(self):
        """
        Build the children for the layout based on the users permissions
        """
        if self._page:
            children = {'page': self._page}
            children.update(self._build_menus())
        else:
            children = {}
        return children

    def _build_menus(self):
        """
        Build the main and sub menus for the application based on modules and pages
        """
        current_page = self._page._data_model
        current_module = current_page.module
        site = current_module.site
        menus = {
            MenuTypes.MAIN: MenuPagelet(label=MenuTypes.MAIN,
                                        selected_item=current_module.title,
                                        selected_sub_item=current_page.title,
                                        request=self.request,
                                        request_kwargs=self.request_kwargs),
            MenuTypes.SIDE: MenuPagelet(label=MenuTypes.SIDE,
                                        selected_item=current_page.title,
                                        request=self.request,
                                        request_kwargs=self.request_kwargs)}

        if not site.private:
            for module in Module.objects.active_site_modules(site).filter(show_in_navigation=True):
                menus[MenuTypes.MAIN].append(module.title, '/%s' % module.name, icon=module.icon)
                for page in Page.objects.active_module_pages(self.request.user, module).filter(show_in_navigation=True):
                    menus[MenuTypes.MAIN].append_sub_item(module.title, page.title, '/%s/%s' % (module.name, page.name),
                                                          icon=page.icon)
            for page in Page.objects.active_module_pages(self.request.user, current_module).filter(
                    show_in_navigation=True):
                menus[MenuTypes.SIDE].append(page.title, '/%s/%s' % (current_module.name, page.name), icon=page.icon)
        else:
            for module in Module.objects.active_user_site_modules(self.request.user, site).filter(
                    show_in_navigation=True):
                menus[MenuTypes.MAIN].append(module.title, '/%s' % module.name, icon=module.icon)
                for page in Page.objects.active_user_module_pages(self.request.user, module).filter(
                        show_in_navigation=True):
                    menus[MenuTypes.MAIN].append_sub_item(module.title, page.title, '/%s/%s' % (module.name, page.name),
                                                          icon=page.icon)
            for page in Page.objects.active_user_module_pages(self.request.user, current_module).filter(
                    show_in_navigation=True):
                menus[MenuTypes.SIDE].append(page.title, '/%s/%s' % (current_module.name, page.name), icon=page.icon)
        return menus

    def index_html(self):
        self._template = ['layout_index.html', self._template]
        return self.html()


class PCLayout(BaseLayout):
    pass
