from .models import Project, Task, Comment, Section
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'members']

class SectionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())  # Use SectionSerializer if you need detailed info
    comments = CommentSerializer(many=True, read_only=True)
    # section_options = SectionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'assigned_to', 'section', 'comments']
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     project_sections = Section.objects.filter(project=instance.project)
    #     representation['section_options'] = SectionOptionSerializer(project_sections, many=True).data
    #     return representation
    
class SectionSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'tasks']

class ProjectDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'members', 'sections']
