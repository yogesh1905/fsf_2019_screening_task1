from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path('', views.team_list, name='teams'),
    # path('create/', views.article_create, name='create'),
    # path('<slug:slug>/', views.article_detail, name='detail'),
    path('create-team/', views.create_team, name="createteam"),  # will make a post request to create-team
    path('<int:gid>/', views.member_list, name="memberlist"),
    # path('add-user/', views.add_user, name="adduser"),
]
