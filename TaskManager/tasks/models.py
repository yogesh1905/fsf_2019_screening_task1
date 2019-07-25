from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (('Planned', 'Planned'), ('Inprogress', 'Inprogress'), ('Done', 'Done'))  

# below model defines a group containing username of the group creator
class Group(models.Model):
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


# below model creates a many to many relationship between user and team (or group) 
class JoinTable(models.Model):
	person_id = models.ForeignKey(User, on_delete=models.CASCADE)
	group_id = models.ForeignKey(Group, on_delete=models.CASCADE)


# below model defines property of a task
class Task(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=400)
	assignee = models.ForeignKey(User, on_delete=models.CASCADE)		# Creator of the task
	status = models.CharField(max_length=100, choices=STATUS_CHOICES)	# There are 3 choices for status
	group_id = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, null=True)   # Set to -1 by default when a task doesn't belong to any group
	def __str__(self):
		return self.title

	def snippet(self):
		return self.description[:50] + '...'


# below model defines the property of a comment
class Comment(models.Model):
	task_id = models.ForeignKey(Task, on_delete=models.CASCADE)		# The id of the task to which the comment belongs to
	comment = models.CharField(max_length=300)
	commenter = models.ForeignKey(User, on_delete=models.CASCADE)
	

# below model defines the users assigned to a given task
class AssignTask(models.Model):
	task_id = models.ForeignKey(Task, on_delete=models.CASCADE)		
	person_id = models.ForeignKey(User, on_delete=models.CASCADE)
