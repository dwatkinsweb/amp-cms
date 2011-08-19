import unittest
from ampcms.tests.mock import Mock, patch 
from ampcms.tests import mock_data

from ampcms.lib.layouts import BaseLayout, MenuTypes
from ampcms.lib.pages import BasePage
from ampcms.lib.pagelets import MenuPagelet
from ampcms.managers import ModuleManager, PageManager
from ampcms.models import Module, Page

mock_page_model_1 = Mock(spec=Page)
mock_page_model_1.name = 'page-2'
mock_page_model_1.title = 'Page 2'
mock_page_model_2 = Mock(spec=Page)
mock_page_model_2.name = 'page-2'
mock_page_model_2.title = 'Page 2'
mock_page_model_3 = Mock(spec=Page)
mock_page_model_3.name = 'page-3'
mock_page_model_3.title = 'Page 3'
mock_user_pages_return = [mock_page_model_1, mock_page_model_2, mock_page_model_3]
mock_user_pages = Mock(return_value=mock_user_pages_return)

mock_module_model_1 = Mock(spec=Module)
mock_module_model_1.name = 'module-1'
mock_module_model_1.title = 'Module 1'
mock_module_model_2 = Mock(spec=Module)
mock_module_model_2.name = 'module-2'
mock_module_model_2.title = 'Module 2'
mock_module_model_3 = Mock(spec=Module)
mock_module_model_3.name = 'module-3'
mock_module_model_3.title = 'Module 3'
mock_user_modules_return = [mock_module_model_1, mock_module_model_2, mock_module_model_3]
mock_user_modules = Mock(return_value=mock_user_modules_return)

mock_page = Mock(spec=BasePage)
mock_page._data_model = mock_page_model_1

class LayoutTest(unittest.TestCase):
    @patch.object(ModuleManager, 'user_modules', mock_user_modules)
    @patch.object(PageManager, 'user_pages', mock_user_pages)
    def test_build_children(self):
        layout = BaseLayout(request=mock_data.mock_request, request_kwargs=None, page=mock_page)
        children = layout._build_children()
        self.assertIn('page', children, 'children does not contain a main menu item')
        self.assertIn(MenuTypes.MAIN, children, 'children does not contain a main menu item')
        self.assertIn(MenuTypes.SIDE, children, 'children does not contain a side menu item')
        self.assertIsInstance(children['page'], BasePage, 'main menu is not a page object')
        self.assertIsInstance(children[MenuTypes.MAIN], MenuPagelet, 'main menu is not a menu pagelet')
        self.assertIsInstance(children[MenuTypes.SIDE], MenuPagelet, 'side menu is not a menu pagelet')
    
    def test_build_children_no_page(self):
        layout = BaseLayout(request=None, request_kwargs=None, page=None)
        children = layout._build_children()
        self.assertDictEqual(children, {}, 'children is not an empty dictionary')

    @patch.object(ModuleManager, 'user_modules', mock_user_modules)
    @patch.object(PageManager, 'user_pages', mock_user_pages)
    def test_build_menus(self):
        layout = BaseLayout(request=mock_data.mock_request, request_kwargs=None, page=mock_page)
        menus = layout._build_menus()
        self.assertIn(MenuTypes.MAIN, menus, 'menus does not contain a main menu item')
        self.assertIn(MenuTypes.SIDE, menus, 'menus does not contain a side menu item')
        self.assertIsInstance(menus[MenuTypes.MAIN], MenuPagelet, 'main menu is not a menu pagelet')
        self.assertIsInstance(menus[MenuTypes.SIDE], MenuPagelet, 'side menu is not a menu pagelet')