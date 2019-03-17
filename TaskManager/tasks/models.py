from django.db import models


STATUS_CHOICES = (('Planned', 'Planned'), ('Inprogress', 'Inprogress'), ('Done', 'Done'))
# Create your models here.
class JoinTable(models.Model):
	person_id = models.IntegerField()
	group_id = models.IntegerField()


class Group(models.Model):
	creator = models.CharField(max_length=100)


class Task(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=400)
	assignee = models.CharField(max_length=100)
	status = models.CharField(max_length=100, choices=STATUS_CHOICES)
	group_id = models.IntegerField(default=-1)
	def __str__(self):
		return self.title

	def snippet(self):
		return self.description[:50] + '...'


class Comment(models.Model):
	task_id = models.IntegerField()
	comment = models.CharField(max_length=300)
	commenter = models.CharField(max_length=100, default="")
	

class AssignTask(models.Model):
	task_id = models.IntegerField()
	person_id = models.IntegerField()
