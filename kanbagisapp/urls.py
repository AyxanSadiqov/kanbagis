from django.conf.urls import url, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from kanbagisapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from .views import ThreadView, InboxView

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^home', views.home, name='home'),
    url(r'^icerik/(?P<id>\d+)/$', views.icerik, name='icerik'),
    url(r'^about', views.hakkimizda, name='hakkimizda'),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^share', views.paylasimdabulun, name='paylasimdabulun'),
    url(r'^ajax/load/$', views.load_counties, name='ajax_load_counties'),
    url(r'^$', views.home, name='home'),
    url(r'^register/', views.register, name='register'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^ajax/validate_email/$', views.validate_email, name='validate_email'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^acil/', views.acil, name='acil'),
    url(r'^conversation$', broadcast),
    url(r'^conversations/$', conversations),
    url(r'^conversations/(?P<id>[-\w]+)/delivered$',delivered),
    url(r'^chat/', views.chat, name='chat'),
    path("inbox/", InboxView.as_view()),
    re_path(r"^messages/(?P<username>[\w.@+-]+)/$", ThreadView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
