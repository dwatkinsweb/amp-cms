import unittest
from ampcms.tests.mock import Mock, patch
from ampcms.tests import mock_data

from ampcms.lib.content_type import BaseContentType

from genshi.core import Markup
from django_genshi import RequestContext

mock_build_children_return = {
    'base': mock_data.MockChild(['base.css']),
    'base2': mock_data.MockChild(['base2a.css', 'base2b.css']),
    'base3': mock_data.MockChild(['base2a.css', 'base3.css'])}
mock_build_children = Mock(return_value=mock_build_children_return)

mock_get_context_return = {'var_a': 'val_a', 'var_b': 'val_b'}
mock_get_context = Mock(return_value=mock_get_context_return)

mock_get_html_data_return = {'data_a': 'val_a', 'data_b': 'val_b'}
mock_get_html_data = Mock(return_value=mock_get_html_data_return)

class BaseContentTypeTest(unittest.TestCase):
    @patch.object(BaseContentType, '_get_context', new=mock_get_context)
    @patch.object(BaseContentType, '_get_template', new=mock_data.mock_get_template_signature)
    def test_html(self):
        content_type = BaseContentType(request=None, request_kwargs=None)
        html = content_type.html()
        self.assertEqual(html, '<p>var_a : val_a. var_b : val_b.</p>', 'html was incorrect: %s' % html)

    @patch.object(BaseContentType, '_get_context', new=mock_get_context)
    @patch.object(BaseContentType, '_get_template', new=mock_data.mock_get_template_signature)
    def test_markup(self):
        content_type = BaseContentType(request=None, request_kwargs=None)
        html = content_type.markup()
        self.assertIsInstance(html, Markup, 'html was not a markup object: %s' % type(html))
        self.assertEqual(html, '<p>var_a : val_a. var_b : val_b.</p>', 'html was incorrect: %s' % html)

    @patch.object(BaseContentType, '_build_children', new=mock_build_children)
    def test_css(self):
        content_type = BaseContentType(request=None, request_kwargs=None)
        css = content_type.css()
        self.assertEquals(css.count('@import url("base.css");'), 1, 'One of the css files was duplicated')
        self.assertIn('@import url("base.css");', css, 'One of the css files was missing')
        self.assertEquals(css.count('@import url("base2a.css");'), 1, 'One of the css files was duplicated')
        self.assertIn('@import url("base2a.css");', css, 'One of the css files was missing')
        self.assertEquals(css.count('@import url("base2b.css");'), 1, 'One of the css files was duplicated')
        self.assertIn('@import url("base2b.css");', css, 'One of the css files was missing')
        self.assertEquals(css.count('@import url("base3.css");'), 1, 'One of the css files was duplicated')
        self.assertIn('@import url("base3.css");', css, 'One of the css files was missing')

    @patch.object(BaseContentType, '_get_html_data', new=mock_get_html_data)
    def test_get_data_tags(self):
        content_type = BaseContentType(request=None, request_kwargs=None)
        data_tags = content_type.get_html_data_tags()
        self.assertDictEqual(data_tags, {'data-data_a':'val_a', 'data-data_b': 'val_b'}, 'data_tags was not the correct dictionary: %s' % data_tags)

    def test_get_template(self):
        content_type = BaseContentType(request=None, request_kwargs=None)
        content_type._template = mock_data.mock_template
        template = content_type._get_template()
        self.assertEquals(template, 'ampcms/%s.html' % mock_data.mock_template, '_get_template() returned incorrect template: %s' % template)

    def test_get_template_none(self):
        content_type = BaseContentType(request=None, request_kwargs=None)
        self.assertRaises(Exception, content_type._get_template)

    @patch.object(BaseContentType, '_build_children', new=mock_build_children)
    @patch.object(BaseContentType, '_get_html_data', new=mock_get_html_data)
    def test_get_context(self):
        content_type = BaseContentType(request=None, request_kwargs=None)
        context = content_type._get_context()
        self.assertIsInstance(context, dict, 'context was not a dictionary')

    @patch.object(BaseContentType, '_build_children', new=mock_build_children)
    @patch.object(BaseContentType, '_get_html_data', new=mock_get_html_data)
    def test_get_context_with_request(self):
        content_type = BaseContentType(request=mock_data.mock_request(), request_kwargs=None)
        context = content_type._get_context()
        self.assertIsInstance(context, RequestContext, 'context was not a dictionary')

