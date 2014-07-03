from django.conf.urls import patterns, include, url
from django.contrib import admin

from polls2 import urls


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include(urls, namespace="polls2"))
)
