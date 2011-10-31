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
