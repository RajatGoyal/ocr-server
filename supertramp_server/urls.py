from django.conf.urls import patterns, include, url
import os
from ocr import urls as ocr_urls
from django.contrib import admin
from supertramp_server.settings import MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'supertramp_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(ocr_urls)),
    url(r'^static(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__),'../static/')}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT})
)