from django.conf.urls import patterns, include, url
from django.contrib import admin
# from rest_framework.authtoken import views 
# from auto_f5.views import f5_views
from auto_f5.views import f5_views
urlpatterns = patterns('',
    # url(r'^auth/', views.obtain_auth_token),
    url(r'^f5/$', f5_views.F5_ObtainAuthToken),
    url(r'^info/$', f5_views.get_vip_info),
    url(r'^search/$', f5_views.search),
    url(r'^node_control/$', f5_views.node_control),
    url(r'^pools/$', f5_views.listpool,name='listpoolurl'),
    url(r'^node_define/(?P<pool_id>\d+)/(?P<node_id>\d+)$',f5_views.node_define, name='node_defineurl'),
)