from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
	
	path('signup/', views.signup_view, name='signup'),  # name = 'signup' => namespacing the url so that it can be used later on
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),

]