from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms

# Current views handles all the requests related to tasks and teams
# @login_required used before every function to make sure that no unauthorized access takes place


# Handles the request for home page of the user
@login_required(login_url="/accounts/login")
def team_list(req):
	tasks = Task.objects.filter(group_id=None, assignee=req.user)

	# Quering for the list of groups the current user belongs to
	usergroups = JoinTable.objects.filter(person_id=req.user)
	group_id_list = []
	for group in usergroups:
		group_id_list.append(group.group_id.id)
	usergroups = Group.objects.filter(id__in=group_id_list)
	
	return render(req, 'tasks/teamlist.html', {'usergroups': usergroups, 'tasks':tasks})



# Handles the post request when a user creates a team
@login_required(login_url="/accounts/login")
def create_team(req):
	if req.method == 'POST':
		# Creates the group and saves it in the database
		newGroup = Group(creator=req.user)
		newGroup.save()
		newEntry = JoinTable(person_id=req.user, group_id=newGroup)
		newEntry.save()
		print('/tasks/' + str(newGroup.id) + '/')
		return render(req, 'tasks/memberlist.html', {'members': [req.user] ,'creator': req.user.username, 'groupid': newGroup.id, 'curruser': req.user.username, 'newTeam': 'yes'})




# Handles the request for the team page (the page containing the details of the respective team) of a user
@login_required(login_url="/accounts/login")
def member_list(req, gid):
	# Checking if the current user belongs to the group with group_id = gid
	group = Group.objects.filter(id=gid)
	if(group):
		group = group[0]
	else:
		group = None
	if JoinTable.objects.filter(group_id=group, person_id=req.user):
		# Quering for the list of users belonging to the current group
		memberIds = JoinTable.objects.filter(group_id=group)
		if memberIds:
			members = []
			for memberId in memberIds:
				members.append(User.objects.filter(id=memberId.person_id.id)[0].username)
			# Quering for the list of task belonging to the current group
			tasks = Task.objects.filter(group_id=group)
			return render(req, 'tasks/memberlist.html', {'members': members, 'creator': group.creator, 'groupid': group.id, 'curruser':req.user.username, 'tasks': tasks})
		else:
			return render(req, 'tasks/404.html')
	else:
		return render(req, 'tasks/404.html')



# Handles the request for the page containing the list of possible users that can be added to the current team 
@login_required(login_url="/accounts/login")
def add_user(req, gid):
	group = Group.objects.filter(id=gid)
	if(group):
		group = group[0]
	else:
		group = None
	if req.method == 'GET':
		# Checking if the current user belongs to the group with group_id = gid
		currmem = JoinTable.objects.filter(group_id=group)
		if currmem:
			# Quering for the list of possible users that can be added
			searchedgrp = group
			if req.user == searchedgrp.creator:
				arr = []
				for i in currmem:
					arr.append(i.person_id.id)
				nousers = User.objects.exclude(id__in=arr)
				return render(req, 'tasks/adduser.html', {'nousers': nousers, 'groupid': group.id})
			else:
				return render(req, 'tasks/404.html')
		else:
			return render(req, 'tasks/404.html')



# Handles the post request when a user tries to add another user to his team	
@login_required(login_url="/accounts/login")
def added(req, gid, pid):
	group = Group.objects.filter(id=gid)
	if(group):
		group = group[0]
	else:
		group = None
	if req.method == 'POST':
		# Saving the user to the database
		newEntry = JoinTable(person_id=User.objects.get(id=pid), group_id=group)
		newEntry.save()
		return redirect('/tasks/' + str(gid) + '/')




# Handles the post and get request for user adding individual task
@login_required(login_url="/accounts/login")
def add_individual_task(req):
	if req.method == 'POST':
		form = forms.CreateTask(req.POST)
		if form.is_valid():
			# save article to db
			instance = form.save(commit=False)
			instance.assignee = req.user
			instance.save()
			return redirect('tasks:teams')
	else:
		form = forms.CreateTask()
	return render(req, 'tasks/createtask.html', {'form': form})	




# Handles the request for page containing the details of individual tasks and also a post request for adding comment
@login_required(login_url="/accounts/login")
def task_detail(req, tid):
	task = Task.objects.filter(id=tid)
	if task and task[0].assignee == req.user:
		task = task[0]
		if req.method == 'GET':
			curr_user = req.user.username
			all_comments = Comment.objects.filter(task_id=task).order_by('-id')
			return render(req, 'tasks/taskdetail.html', {'task': task, 'curr_user': curr_user, 'all_comments': all_comments})
		else:
			newComment = Comment(task_id=tid, comment=req.POST.get('comment'), commenter=req.user.username)
			# Saving the comment to the db
			newComment.save()
			return redirect('/tasks/view-task/' + str(tid) + '/')

	else:
		return render(req, 'tasks/404.html')
	



# Handles the get and post request for user wanting to edit a task
@login_required(login_url="/accounts/login")
def edit_task(req, tid):
	task = Task.objects.filter(id=tid)
	if task:
		task = task[0]
		if task.assignee == req.user:
			if req.method == 'POST':
				form = forms.CreateTask(req.POST)
				if form.is_valid():
					# save the edited article to db
					instance = Task.objects.filter(id=tid)[0]
					instance.title = req.POST.get("title")
					instance.status = req.POST.get("status")
					instance.description = req.POST.get("description")
					instance.save()
					return redirect('tasks:teams')
			else:
				form = forms.CreateTask()
			return render(req, 'tasks/edittask.html', {'form': form, 'taskId': tid})
		else:
			return render(req, 'tasks/404.html')
	else:
		return render(req, 'tasks/404.html')



# Handles the request for a member belonging to a team and wanting to add a task in the team
@login_required(login_url="/accounts/login")
def add_group_task(req, gid):
	group = Group.objects.filter(id=gid)
	if(group):
		group = group[0]
	else:
		group = None
	curruser = JoinTable.objects.filter(group_id=group, person_id=req.user)
	# Checking if the current user belongs to the team
	if curruser:
		if req.method == 'POST':
			form = forms.CreateTask(req.POST)
			if form.is_valid():
				# saving article to db
				instance = form.save(commit=False)
				instance.assignee = req.user
				instance.group_id = group
				instance.save()
				return redirect('/tasks/' + str(gid) + '/')
		else:
			form = forms.CreateTask()
		return render(req, 'tasks/create_group_task.html', {'form': form, 'group_id': gid})

	else:
		return render(req, 'tasks/404.html')




# Handles the request for page containing the details of a task belonging to a particular team
@login_required(login_url="/accounts/login")
def group_task_detail(req, gid, tid):
	group = Group.objects.filter(id=gid)
	if(group):
		group = group[0]
	else:
		group = None
	task = Task.objects.filter(id=tid, group_id=group)
	curr = JoinTable.objects.filter(group_id=group, person_id=req.user)
	# Checking if the task and group exist and the task belongs to that group
	if task and curr:
		task = task[0]
		curr = curr[0]
		if req.method == 'GET':
			assigned_users = AssignTask.objects.filter(task_id=task)
			id_list = []
			for user in assigned_users:
				id_list.append(user.person_id.id)
			assigned_users = User.objects.filter(id__in=id_list)
			curr_user = req.user
			all_comments = Comment.objects.filter(task_id=task).order_by('-id')
			return render(req, 'tasks/group_task_detail.html', {'task': task, 'curr_user': curr_user, 'group_id':gid, 'task_id': tid, 'assigned_users': assigned_users, 'all_comments': all_comments})
		else:
			newComment = Comment(task_id=task, comment=req.POST.get('comment'), commenter=req.user)
			newComment.save()
			return redirect('/tasks/' + str(gid) + '/view-task/' + str(tid) + '/')
	else:
		return render(req, 'tasks/404.html')	




# Handles the request for a member belong to a team and wanting to edit a team task
@login_required(login_url="/accounts/login")
def group_edit_task(req, gid, tid):
	group = Group.objects.filter(id=gid)
	if(group):
		group = group[0]
	else:
		group = None
	task = Task.objects.filter(id=tid, group_id=group)
	# Checking if the task exists
	if task:
		task = task[0]
		if task.assignee == req.user:
			if req.method == 'POST':
				form = forms.CreateTask(req.POST)
				if form.is_valid():
					# saving the edited instance ot the article to db
					instance = Task.objects.filter(id=tid)[0]
					instance.title = req.POST.get("title")
					instance.status = req.POST.get("status")
					instance.description = req.POST.get("description")
					instance.save()
					return redirect('/tasks/' + str(gid) + '/')
			else:
				form = forms.CreateTask()
			return render(req, 'tasks/group_edit_task.html', {'form': form, 'task_id': tid, 'group_id': gid})
		else:
			return render(req, 'tasks/404.html')
	else:
		return render(req, 'tasks/404.html')	




# Handles the get request of a task creator wanting to assign a task to the members of the team
@login_required(login_url="/accounts/login")
def group_assign_task(req, gid, tid):
	group = Group.objects.filter(id=gid)
	if(group):
		group = group[0]
	else:
		group = None
	task = Task.objects.filter(id=tid, group_id=group)
	if task:
		task = task[0]
		# Checking if the current user is the creator of the task
		if task.assignee == req.user:
			already_assigned = AssignTask.objects.filter(task_id=task)
			assigned_id = []
			for person in already_assigned:
				assigned_id.append(person.person_id.id)	
			not_assigned_list = User.objects.exclude(id__in=assigned_id)
			not_assigned = JoinTable.objects.filter(person_id__in=not_assigned_list, group_id=group)
			temp_id = []
			for user in not_assigned:
				temp_id.append(user.person_id.id)
			not_assigned = User.objects.filter(id__in=temp_id)
			return render(req, 'tasks/assign_user.html', {'not_assigned': not_assigned, 'group_id': gid, 'task_id': tid})
		else:
			return render(req, 'tasks/404.html')
	else:
		return render(req, 'tasks/404.html')




# Handles the post request of a task creator wanting to assign a task to the members of the team 
@login_required(login_url="/accounts/login")
def group_task_assigned(req, gid, tid, pid):
	assigned_user = AssignTask(task_id=Task.objects.get(id=tid), person_id=User.objects.get(id=pid))
	assigned_user.save()
	return redirect('/tasks/' + str(gid) + '/view-task/' + str(tid) + '/')






