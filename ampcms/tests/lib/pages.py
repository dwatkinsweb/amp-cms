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

import unittest
from ampcms.tests.mock import Mock, patch
from ampcms.tests import mock_data

from ampcms.lib.pages import BasePage, PageletPage
from ampcms.lib.pagelets import BasePagelet
from ampcms.models import Page, Pagelet

mock_pagelet_model_1 = Mock(spec=Pagelet, name="mock 1")
mock_pagelet_model_1.name = 'pagelet-1'
mock_pagelet_model_1.pagelet_class = 'SimplePagelet'
mock_pagelet_model_2 = Mock(spec=Pagelet, name="mock 2")
mock_pagelet_model_2.name = 'pagelet-2'
mock_pagelet_model_2.pagelet_class = 'ApplicationPagelet'
mock_pagelet_model_3 = Mock(spec=Pagelet, name="mock 3")
mock_pagelet_model_3.name = 'pagelet-3'
mock_pagelet_model_3.pagelet_class = 'SimplePagelet'

mock_page_model = Mock(spec=Page)
mock_page_model.name = 'Mock Page'
mock_get_absolute_url_return = 'http://sb-www.agentportal.com/page/module_name/page_name'
mock_get_absolute_url = Mock(return_value=mock_get_absolute_url_return)
mock_page_model.get_absolute_url = mock_get_absolute_url
mock_active_pagelets_return = [mock_pagelet_model_1, mock_pagelet_model_2, mock_pagelet_model_3]
mock_page_model.active_pagelets = Mock(return_value=mock_active_pagelets_return)

class PageTest(unittest.TestCase):
    @patch.object(BasePage, 'get_absolute_url', new=mock_get_absolute_url)
    def test_get_html_data(self):
        page = BasePage(request=mock_data.mock_request, request_kwargs={}, page=mock_page_model)
        data = page._get_html_data()
        expected_data = {'url': mock_get_absolute_url_return, 'name': mock_page_model.name}
        self.assertDictEqual(expected_data, data, 'data was incorrect %s' % data)

    def test_get_absolute_url(self):
        page = BasePage(request=mock_data.mock_request, request_kwargs={}, page=mock_page_model)
        url = page.get_absolute_url()
        self.assertEqual(mock_get_absolute_url_return, url, 'url is incorrect %s' % url)

class PageletPageTest(unittest.TestCase):
    def test_get_pagelet(self):
        page = PageletPage(request=mock_data.mock_request, request_kwargs={}, page=mock_page_model)
        pagelet = page.get_pagelet(mock_pagelet_model_2.name)
        self.assertIs(pagelet._data_model, mock_pagelet_model_2, 'got incorrect pagelet %s' % pagelet)

    def test_get_pagelet_no_key(self):
        page = PageletPage(request=mock_data.mock_request, request_kwargs={}, page=mock_page_model)
        pagelet = page.get_pagelet()
        self.assertIsInstance(pagelet, BasePagelet, 'pagelet was not a Pagelet %s' % pagelet)

    def test_get_pagelet_not_found(self):
        page = PageletPage(request=mock_data.mock_request, request_kwargs={}, page=mock_page_model)
        pagelet = page.get_pagelet('test')
        self.assertIsNone(pagelet, 'pagelet was not none %s' % pagelet)

    def test_build_children(self):
        page = PageletPage(request=mock_data.mock_request, request_kwargs={}, page=mock_page_model)
        children = page._build_children()
        self.assertEqual(len(children), len(mock_active_pagelets_return), 'incorrect number of children returned')
        self.assertIn(mock_pagelet_model_1.name, children, '%s not in children' % mock_pagelet_model_1.name)
        self.assertIsInstance(children[mock_pagelet_model_1.name], BasePagelet, '%s not a pagelet' % mock_pagelet_model_1.name)
        
