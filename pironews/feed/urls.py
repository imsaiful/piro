from django.conf.urls import url
from . import views

app_name = 'feed'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'republic/$',views.republic, name='republic'),
    url(r'indiatv/$', views.indiatv, name='indiatv'),
    url(r'ndtv/$', views.ndtv, name='ndtv'),
    url(r'statistics/$', views.ndtv, name='stats'),
    url(r'republic/home/$', views.Republic_Home, name='republichome'),
    url(r'hindustan/home/$', views.Hindustan_Home, name='hindustanhome'),
    url(r'ndtv/home/$', views.Ndtv_Home, name='ndtvhome'),
]
