from django.test import TestCase
from django.test.utils import setup_test_environment
setup_test_environment()

class ModuleManagerTest(TestCase):
    fixtures = ['test.json']
    
    def test_active_by_site(self):
        pass

    def test_user_modules(self):
        pass

class PageManagerTest(TestCase):
    pass

class PageletManagerTest(TestCase):
    pass

class SiteManagerTest(TestCase):
    pass