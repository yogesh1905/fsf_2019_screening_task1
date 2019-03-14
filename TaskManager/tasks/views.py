from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms


# Create your views here.
@login_required(login_url="/accounts/login")
def team_list(req):
	tasks = Task.objects.filter(group_id=-1, assignee=req.user.username)
	print(tasks)
	usergroups = JoinTable.objects.filter(person_id=req.user.id)
	return render(req, 'tasks/teamlist.html', {'usergroups': usergroups, 'tasks':tasks})

@login_required(login_url="/accounts/login")
def create_team(req):
	print(req.method)
	if req.method == 'POST':
		newGroup = Group(creator=req.user.username)
		newGroup.save()
		newEntry = JoinTable(person_id=req.user.id, group_id=newGroup.id)
		newEntry.save()
		print('/tasks/' + str(newGroup.id) + '/')
		return redirect('/tasks/' + str(newGroup.id) + '/')

@login_required(login_url="/accounts/login")
def member_list(req, gid):
	if JoinTable.objects.filter(group_id=gid, person_id=req.user.id):
		memberIds = JoinTable.objects.filter(group_id=gid)
		group = Group.objects.filter(id=gid)
		if group:
			group = group[0]
		if memberIds:
			members = []
			for memberId in memberIds:
				members.append(User.objects.filter(id=memberId.person_id)[0].username)
			return render(req, 'tasks/memberlist.html', {'members': members, 'creator': group.creator, 'groupid': gid, 'user':req.user.username})
		else:
			return HttpResponse('Page Not Found')
	else:
		return HttpResponse("Not Authorized")


@login_required(login_url="/accounts/login")
def add_user(req, gid):
	if req.method == 'GET':
		currmem = JoinTable.objects.filter(group_id=gid)
		if currmem:
			searchedgrp = Group.objects.filter(id=gid)[0]
			if req.user.username == searchedgrp.creator:
				arr = []
				for i in currmem:
					arr.append(i.person_id)
				nousers = User.objects.exclude(id__in=arr)
				return render(req, 'tasks/adduser.html', {'nousers': nousers, 'groupid': gid})
			else:
				return HttpResponse('Not Authorized')
		else:
			return HttpResponse('Group Does Not exist')

	
@login_required(login_url="/accounts/login")
def added(req, gid, pid):
	if req.method == 'POST':
		newEntry = JoinTable(person_id=pid, group_id=gid)
		newEntry.save()
		return redirect('/tasks/' + str(gid) + '/')


@login_required(login_url="/accounts/login")
def add_individual_task(req):
	if req.method == 'POST':
		form = forms.CreateTask(req.POST)
		# req.POST = req.POST.copy()
		# req.POST['assignee'] = req.user.username
		if form.is_valid():
			# save article to db
			instance = form.save(commit=False)
			instance.assignee = req.user.username
			instance.save()
			return redirect('tasks:teams')
	else:
		form = forms.CreateTask()
	return render(req, 'tasks/createtask.html', {'form': form})




@login_required(login_url="/accounts/login")
def task_detail(req, tid):
	task = Task.objects.filter(id=tid)
	if task:
		task = task[0]
		curr_user = req.user.username
		return render(req, 'tasks/taskdetail.html', {'task': task, 'curr_user': curr_user})
	else:
		return HttpResponse("Task does not exists")


@login_required(login_url="/accounts/login")
def edit_task(req, tid):
	if req.method == 'POST':
		form = forms.CreateTask(req.POST)
		# req.POST = req.POST.copy()
		# req.POST['assignee'] = req.user.username
		if form.is_valid():
			# save article to db
			instance = Task.objects.filter(id=tid)[0]
			instance.title = req.POST.get("title")
			instance.status = req.POST.get("status")
			instance.description = req.POST.get("description")
			instance.save()
			return redirect('tasks:teams')
	else:
		form = forms.CreateTask()
	return render(req, 'tasks/edittask.html', {'form': form, 'taskId': tid}, )	
