from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django import forms


# Create your views here.
@login_required(login_url="/accounts/login")
def team_list(req):
	users = User.objects.all()
	return render(req, 'tasks/teamlist.html', {'users': users})

def team_info(req):
	return HttpResponse('Are you amazed?')

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

