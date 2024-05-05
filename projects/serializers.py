from rest_framework import serializers
from .models import Project, Task

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'members']

class TaskSerializer(serializers.ModelSerializer):
    # Nested Project Serializer
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'status', 'due_date', 'assigned_to']
