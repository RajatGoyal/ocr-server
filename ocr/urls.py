__author__ = 'rajatgoyal'

from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from api import Task


v1_api = Api(api_name='v1')
v1_api.register(Task())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/',include(admin.site.urls), name='admin'),
]