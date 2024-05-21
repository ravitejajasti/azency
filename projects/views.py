from django.views.generic import ListView
from .models import Project, Task, Section, Comment
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from .forms import TaskForm
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render


###### API related Classes


from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project, Task, Section
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.annotate(total_tasks=Count('tasks'))
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProjectRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        serializer.save(project=project)

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class SectionTaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(section__project_id=self.kwargs['project_id'])

class TaskDetailView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if 'X-Requested-With' in request.headers:
            return Response({
                'success': True,
                'redirect_url': self.get_success_url(instance),
                'message': 'Task updated successfully.',
                'pk': instance.pk,
            })

        return Response(serializer.data)

    def get_success_url(self, instance):
        return reverse_lazy('projects:task_detail', kwargs={'project_id': instance.project.id, 'pk': instance.pk})

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs['pk'])
        serializer.save(task=task)




class TaskDeleteAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        task_id = kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id, project_id=project_id)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
