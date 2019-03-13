from django.contrib import admin
from .models import JoinTable, Task, Comment

# Register your models here.
admin.site.register(JoinTable)
admin.site.register(Task)
admin.site.register(Comment)
