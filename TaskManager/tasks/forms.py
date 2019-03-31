from django import forms
from . import models


# Form for creating and editing a task
class CreateTask(forms.ModelForm):
	class Meta:
		model = models.Task
		fields = ['title', 'description', 'status']
