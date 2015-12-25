from django.conf.urls import url

from . import views, ajax_views



app_name = 'pfinance'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login_verify/$', views.login_verify, name='login_verify'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^add_tran/$', views.add_tran, name='add_tran'),
]
