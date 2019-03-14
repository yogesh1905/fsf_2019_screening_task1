from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path('', views.team_list, name='teams'),
    path('create-team/', views.create_team, name="createteam"),  # will make a post request to create-team
    path('<int:gid>/', views.member_list, name="memberlist"),
    path('<int:gid>/add-user/', views.add_user, name="adduser"),
   	path('<int:gid>/add-user/<int:pid>/', views.added, name="added"),
   	path('add-task/', views.add_individual_task, name="indtask"),
   	path('view-task/<int:tid>/', views.task_detail, name="taskdetail"),
   	path('edit-task/<int:tid>/', views.edit_task, name='edittask'),
]
