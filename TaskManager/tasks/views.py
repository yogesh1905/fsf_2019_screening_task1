from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django import forms


# Create your views here.
@login_required(login_url="/accounts/login")
def team_list(req):
	usergroups = JoinTable.objects.filter(person_id=req.user.id)
	return render(req, 'tasks/teamlist.html', {'usergroups': usergroups})

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
	memberIds = JoinTable.objects.filter(group_id=gid)
	group = Group.objects.filter(id=gid)
	if group:
		group = group[0]
	if memberIds:
		members = []
		for memberId in memberIds:
			members.append(User.objects.filter(id=memberId.person_id)[0].username)
		return render(req, 'tasks/memberlist.html', {'members': members, 'creator': group.creator})
	else:
		return HttpResponse('Page Not Found')
# def article_detail(req, slug):
# 	#return HttpResponse(slug)
# 	article = Article.objects.get(slug=slug)
# 	return render(req, 'articles/article_detail.html', {'article': article})


# @login_required(login_url="/accounts/login")    # even "accounts:login" would have worked
# def article_create(req):
# 	if req.method == 'POST':
# 		form = forms.CreateArticle(req.POST, req.FILES)
# 		if form.is_valid():
# 			# save article to db
# 			instance = form.save(commit=False)
# 			instance.author = req.user
# 			instance.save()
# 			return redirect('articles:list')
# 	else:
# 		form = forms.CreateArticle()
# 	return render(req, 'articles/article_create.html', {'form': form})

