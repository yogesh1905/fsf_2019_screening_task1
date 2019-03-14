from django.db import models

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
	status = models.CharField(max_length=100)
	group_id = models.IntegerField(default=-1)


class Comment(models.Model):
	task_id = models.IntegerField()
	comment = models.CharField(max_length=300)
	commenter = models.CharField(max_length=100, default="")
	

