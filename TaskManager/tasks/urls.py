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
   	path('<int:gid>/add-task/', views.add_group_task, name="grptask"),
   	path('<int:gid>/view-task/<int:tid>', views.group_task_detail, name="grptaskdetail"),
   	# path('<int:gid>/edit-task/<int:tid>', views.group_edit_task, name="grpedittask"),
]
