from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homePage, name="home"),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
]

urlpatterns += staticfiles_urlpatterns()