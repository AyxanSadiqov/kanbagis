from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from kanbagisapp import views as kanbagisapp_views
from django.conf.urls import handler404, handler500

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('kanbagisapp.urls'))
]


admin.site.site_header = 'Kan Bağış Admin'
admin.site.index_title = 'Kan Bağışı'  
admin.site.site_title = 'Admin Sayfası'
