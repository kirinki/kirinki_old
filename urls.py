# This file is part of Kirinki.
# 
# Kirinki is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as 
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# Kirinki is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public
# License along with kirinki. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Example
                       # (r'^rstreaming/', include('rstreaming.foo.urls')),
                       
                       # Uncomment the admin/doc line below to enable admin documentation
                       # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin
                       (r'^/*', include('kirinki.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       )
