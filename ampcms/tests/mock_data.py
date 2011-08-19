import os

from ampcms.tests.mock import Mock, mocksignature
from ampcms.lib.content_type import BaseContentType
from ampcms.models import User

from django.http import HttpRequest

class MockChild(object):
    def __init__(self, css):
        self.css = css
    def _build_css(self):
        return self.css

mock_template = 'templates/content_object_test'
mock_get_template_return = os.path.join(__file__, '..', mock_template+'.html')
mock_get_template = Mock(return_value=mock_get_template_return)
mock_get_template_signature = mocksignature(BaseContentType._get_template, mock_get_template)

mock_user = Mock(spec=User)
mock_request = Mock(wraps=HttpRequest)
mock_request.user = mock_user