from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cond_index, name='cond_index'),
    url(r'^enquire/$', views.cond_enq, name='cond_enq'),
    url(r'^home/$', views.cond_home, name='cond_home'),
    url(r'^updt/$', views.cond_updt, name='cond_updt'),
    url(r'^getlpp/$', views.get_lpp, name='get_lpp'),
    url(r'^admin/conditions/$', views.go_admin, name='go_admin'),
]