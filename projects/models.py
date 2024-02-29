from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import datetime

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_created')
    members = models.ManyToManyField(User, related_name='projects_joined')

    def save(self, *args, **kwargs):
        DEFAULT_SECTIONS = ['Todo', 'In Progress', 'Review', 'Complete']

        is_new = self._state.adding
        super(Project, self).save(*args, **kwargs)
        if is_new:
            for section_name in DEFAULT_SECTIONS:
                Section.objects.create(name=section_name, project=self)

class Section(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = (
        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_tasks')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks_assigned')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Incomplete')
    due_date = models.DateField(default=datetime.date.today)
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks_modified')

    def save(self, *args, **kwargs):
        # Custom save method to potentially do something special when a task is saved
        super(Task, self).save(*args, **kwargs)

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.created_at}"

class File(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.file.name
