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

from genshi.core import Markup
from django.http import HttpResponse
from ampcms.lib.pagelets import BasePagelet, MenuPagelet, SimplePagelet, ApplicationPagelet
from ampcms.lib.application_mapper import AmpCmsApplication, application_mapper
from ampcms.models import Pagelet

from django.conf import settings

import json

mock_pagelet_model = Mock(spec=Pagelet)
mock_pagelet_model.name = 'Mock Pagelet Name'
mock_pagelet_model.title = 'Mock Pagelet Title'
mock_pagelet_model.css_files = 'test1.css, test2.css'
mock_pagelet_model.js_files = 'test1.js, test2.js'
expected_css = ['test1.css', 'test2.css']
expected_js = ['test1.js', 'test2.js']

mock_pagelet_model_content = 'This is the test content'
mock_pagelet_model_application = 'test'
mock_pagelet_model_starting_url = 'test/index'

mock_menu_item_1 = 'mock-item 1'
mock_menu_url_1 = 'sb-www.blah.com/test'
mock_menu_label = 'Mock Menu'
mock_menu_selected_item = mock_menu_item_1

mock_urlconf_test_application = 'test.urls'
mock_resolve_response = Mock(spec=HttpResponse)
mock_resolve_response.content = mock_pagelet_model_content
mock_view = Mock(return_value=mock_resolve_response)
mock_args = []
mock_kwargs = {}
mock_resolve_return = (mock_view, mock_args, mock_kwargs)
mock_resolve = Mock(return_value=mock_resolve_return)

class BasePageletTest(unittest.TestCase):
    def test_get_html_data(self):
        pagelet = BasePagelet(request=mock_data.mock_request(), request_kwargs=None, pagelet=mock_pagelet_model)
        data = pagelet._get_html_data()
        self.assertIn('name', data, 'data does not include a name %s' % data)

    def test_build_css(self):
        pagelet = BasePagelet(request=mock_data.mock_request(), request_kwargs=None, pagelet=mock_pagelet_model)
        css = pagelet._build_css()
        self.assertListEqual(expected_css, css, 'css was incorrect %s' % css)

    def test_build_js(self):
        pagelet = BasePagelet(request=mock_data.mock_request(), request_kwargs=None, pagelet=mock_pagelet_model)
        js = pagelet._build_js()
        self.assertListEqual(expected_js, js, 'css was incorrect %s' % js)

class MenuPageletTest(unittest.TestCase):
    def test_append(self):
        pagelet = MenuPagelet(request=mock_data.mock_request(), request_kwargs=None)
        pagelet.append(mock_menu_item_1, mock_menu_url_1)
        self.assertIn((mock_menu_item_1, mock_menu_url_1), pagelet._children, 'did not append item to menu')

    def test_get_context(self):
        pagelet = MenuPagelet(request=mock_data.mock_request(), request_kwargs={}, 
                              menu_label=mock_menu_label, selected_item=mock_menu_selected_item)
        context = pagelet._get_context()
        self.assertIn('menu_label', context, 'context did not contain menu_label')
        self.assertIn('selected_item', context, 'context did not contain selected_item')
        self.assertEqual(mock_menu_label, context['menu_label'], 'context contained incorrect menu_label')
        self.assertEqual(mock_menu_selected_item, context['selected_item'], 'context contained incorrect selected_item')

    def test_get_html_data(self):
        pagelet = MenuPagelet(request=mock_data.mock_request(), request_kwargs={}, 
                              menu_label=mock_menu_label, selected_item=mock_menu_selected_item)
        data = pagelet._get_html_data()
        expected_data = {'name': mock_menu_label}
        self.assertDictEqual(expected_data, data, 'data was incorrect %s' % data)

    def test_build_css(self):
        pagelet = MenuPagelet(request=mock_data.mock_request(), request_kwargs={}, 
                              menu_label=mock_menu_label, selected_item=mock_menu_selected_item)
        css = pagelet._build_css()
        expected_css = ['%scss/%s.css' % (settings.AMPCMS_MEDIA_URL, mock_menu_label)]
        self.assertListEqual(expected_css, css, 'css was incorrect %s' % css)

class SimplePageletTest(unittest.TestCase):
    def setUp(self):
        mock_pagelet_model.content = mock_pagelet_model_content

    def tearDown(self):
        del mock_pagelet_model.content
         
    def test_get_context(self):
        pagelet = SimplePagelet(request=mock_data.mock_request(), request_kwargs={}, pagelet=mock_pagelet_model,
                                menu_label=mock_menu_label, selected_item=mock_menu_selected_item)
        context = pagelet._get_context()
        self.assertIn('content', context, 'context did not contain content %s' % context)
        self.assertIsInstance(context['content'], Markup, 'content was not markup')
        self.assertEqual(context['content'], mock_pagelet_model.content, 'content was incorrect %s' % context['content'])

class ApplicationPageletTest(unittest.TestCase):
    def setUp(self):
        mock_pagelet_model.application = mock_pagelet_model_application
        mock_pagelet_model.starting_url = mock_pagelet_model_starting_url
        mock_pagelet_model.classes = None
        test_application = AmpCmsApplication('test.urls')
        application_mapper.register('test', test_application)
        self.test_item = ('test', test_application)

    def tearDown(self):
        del mock_pagelet_model.application
        del mock_pagelet_model.starting_url
        del mock_pagelet_model.classes
        application_mapper.items.remove(self.test_item)

    @unittest.skip('incomplete')
    def test_html(self):
        #FIXME: test html() function
        pass

    @unittest.skip('incomplete')
    def test_to_stream(self):
        #FIXME: test _to_stream() function
        pass

    @patch('ampcms.lib.pagelets.resolve', mock_resolve)
    def test_get_context_with_content(self):
        pagelet = ApplicationPagelet(request=mock_data.mock_request(), request_kwargs={}, pagelet=mock_pagelet_model,
                                     menu_label=mock_menu_label, selected_item=mock_menu_selected_item)
        context = pagelet._get_context(include_content=True)
        #mock_resolve.assert_called_once_with(mock_pagelet_model_starting_url, mock_urlconf_test_application)
        self.assertIn('content', context, 'context did not contain content %s' % context)
        self.assertIsInstance(context['content'], Markup, 'content was not markup')
        self.assertEqual(context['content'], mock_resolve_response.content, 'content was incorrect %s' % context['content'])

    @patch('ampcms.lib.pagelets.resolve', mock_resolve)
    def test_get_context_no_content(self):
        pagelet = ApplicationPagelet(request=mock_data.mock_request(), request_kwargs={}, pagelet=mock_pagelet_model,
                                     menu_label=mock_menu_label, selected_item=mock_menu_selected_item)
        context = pagelet._get_context()
        self.assertNotIn('content', context, 'context incorrectly contained content %s' % context)

    @patch('ampcms.lib.pagelets.resolve', mock_resolve)
    def test_json(self):
        pagelet = ApplicationPagelet(request=mock_data.mock_request(), request_kwargs={}, pagelet=mock_pagelet_model,
                                     menu_label=mock_menu_label, selected_item=mock_menu_selected_item)
        json_output = pagelet.json()
        json_output = json.loads(json_output)
        #FIXME: Should check for html
        expected_json_output = {'location': mock_pagelet_model_starting_url,
                                'css': expected_css,
                                'js': expected_js}
        self.assertDictContainsSubset(expected_json_output, json_output, 'json was incorrect %s' % json_output)

    @patch('ampcms.lib.pagelets.resolve', mock_resolve)
    def test_build_content(self):
        pagelet = ApplicationPagelet(request=mock_data.mock_request(), request_kwargs={}, pagelet=mock_pagelet_model,
                                     menu_label=mock_menu_label, selected_item=mock_menu_selected_item)
        content = pagelet._build_content()
        #mock_resolve.assert_called_once_with(mock_pagelet_model_starting_url, mock_urlconf_test_application)
        self.assertIsInstance(content, Markup, 'content was not markup')
        self.assertEqual(content, mock_resolve_response.content, 'content was incorrect %s' % content)

    def test_get_html_data(self):
        pagelet = ApplicationPagelet(request=mock_data.mock_request(), request_kwargs={}, pagelet=mock_pagelet_model,
                                     menu_label=mock_menu_label, selected_item=mock_menu_selected_item)
        data = pagelet._get_html_data()
        expected_data = {'starting_url' : mock_pagelet_model_starting_url,
                         'application' : mock_pagelet_model_application}
        self.assertDictContainsSubset(expected_data, data, 'data was missing expceted values %s' % data)
