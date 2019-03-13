#Contains set of all callback functions to execute

from django.http import HttpResponse
from django.shortcuts import render


def homePage(req):
	return render(req, 'homepage.html')

