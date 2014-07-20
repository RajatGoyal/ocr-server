from django.conf.urls import patterns, include, url
from ocr import urls as ocr_urls
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'supertramp_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^ocr/', include(ocr_urls)),
)
