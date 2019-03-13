from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path('', views.team_list, name='teams'),
    # path('create/', views.article_create, name='create'),
    # path('<slug:slug>/', views.article_detail, name='detail'),
    path('team/', views.team_info)
]
