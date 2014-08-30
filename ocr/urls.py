__author__ = 'rajatgoyal'

from django.conf.urls import patterns,include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from api import Task, UserResource, CreateUserResource


v1_api = Api(api_name='v1')
v1_api.register(Task())
v1_api.register(UserResource())
v1_api.register(CreateUserResource())

urlpatterns = patterns('ocr.views',
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/',include(admin.site.urls), name='admin'),
    )


urlpatterns += patterns('ocr.views',
    url(r'^$', 'home', name='home'),
    url(r'^signup', 'signup', name='signup'),
    url(r'^signin', 'signin', name='signin'),
)
