from django.db import models


STATUS_CHOICES = (('Planned', 'Planned'), ('Inprogress', 'Inprogress'), ('Done', 'Done'))  

# below model creates a many to many relationship between user and team (or group) 
class JoinTable(models.Model):
	person_id = models.IntegerField()
	group_id = models.IntegerField()


# below model defines a group containing username of the group creator
class Group(models.Model):
	creator = models.CharField(max_length=100)


# below model defines property of a task
class Task(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=400)
	assignee = models.CharField(max_length=100)		# Creator of the task
	status = models.CharField(max_length=100, choices=STATUS_CHOICES)	# There are 3 choices for status
	group_id = models.IntegerField(default=-1)   # Set to -1 by default when a task doesn't belong to any group
	def __str__(self):
		return self.title

	def snippet(self):
		return self.description[:50] + '...'


# below model defines the property of a comment
class Comment(models.Model):
	task_id = models.IntegerField()		# The id of the task to which the comment belongs to
	comment = models.CharField(max_length=300)
	commenter = models.CharField(max_length=100, default="")
	

# below model defines the users assigned to a given task
class AssignTask(models.Model):
	task_id = models.IntegerField()		
	person_id = models.IntegerField()
