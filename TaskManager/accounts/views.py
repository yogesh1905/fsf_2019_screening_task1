from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# list of views for current app


# Handles user signup
def signup_view(req):
	if req.method == 'POST':
		form = UserCreationForm(req.POST)
		if form.is_valid():
			user = form.save()
			# log the user in
			login(req, user)
			return redirect('tasks:teams')
	else:
		form = UserCreationForm()
		
	return render(req, 'accounts/signup.html', {'form': form})



# Handles user login
def login_view(req):
	if req.method == 'POST':
		form = AuthenticationForm(data=req.POST)
		if form.is_valid():
			# login the user
			user = form.get_user()
			login(req, user)
			if 'next' in req.POST:
				return redirect(req.POST.get('next'))
			else:
				return redirect('tasks:teams') 

	else:
		form = AuthenticationForm()

	return render(req, 'accounts/login.html', {'form': form, 'nxt': req.GET.get('next')})



# Handles user logout
def logout_view(req):
	if req.method == 'POST':
		logout(req)
		return redirect('/')
 