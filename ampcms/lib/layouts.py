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
        self._template = 'layout'

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