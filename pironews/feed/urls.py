from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'republic/$',views.republic, name='republic'),
    url(r'indiatv/$', views.indiatv, name='indiatv'),
    url(r'ndtv/$', views.ndtv, name='ndtv'),

]
