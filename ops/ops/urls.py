from django.conf.urls import patterns, include, url

from django.contrib import admin
from ops01.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$','django.contrib.auth.views.login',{'template_name':'login.html'}),
    url(r'^$',index),
    url(r'^login/$',login),
    url(r'^login_auth/$',login_auth),
    url(r'^logout/$',logout),
    url(r'^getGroupSummary/$',getGroupSummary),
)
