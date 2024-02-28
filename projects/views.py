from django.views.generic import ListView
from .models import Project, Task, Section
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from .forms import TaskForm
from django.contrib.auth.models import User
from django.db.models import Count

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    #login_url = '/login/'  # Redirect to this URL if not logged in

    template_name = 'projects/project_list.html'

    def get_queryset(self):
        # Annotate each project with the count of related tasks
        return Project.objects.annotate(total_tasks=Count('tasks'))

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'description', 'members']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the project's creator to the current user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        
        # When creating a new project, all users are potential members
        all_users = User.objects.all()

        # Adjust context for the template
        context['all_users'] = all_users
        context['current_members'] = User.objects.none()  # No current members for a new project

        return context
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'description', 'members']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('pk')
        if project_id:
            project = Project.objects.get(pk=project_id)
            current_members = project.members.all()
        else:
            current_members = User.objects.none()
        
        all_users = User.objects.all()
        non_members = all_users.exclude(id__in=current_members.values_list('id', flat=True))

        context['current_members'] = current_members
        context['non_members'] = non_members
        return context

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'projects/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs['project_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'projects/task_detail.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'projects/task_form.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['project_id'] = self.kwargs.get('project_id')  # Assume URL captures project_id
        return kwargs

    def get_success_url(self):
        return reverse_lazy('task_list', kwargs={'project_id': self.object.project.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass project_id to the template to maintain the context
        context['project_id'] = self.kwargs.get('project_id')
        return context

    def form_valid(self, form):
        # Associate the task with the project before saving
        project_id = self.kwargs.get('project_id')
        form.instance.project = get_object_or_404(Project, id=project_id)
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    #fields = ['title', 'description', 'status', 'due_date', 'assigned_to', 'parent', 'section']
    form_class = TaskForm
    template_name = 'projects/task_form.html'

    def get_form_kwargs(self):
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs['project_id'] = self.object.project_id
        return kwargs

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'project_id': self.object.project.id, 'pk': self.object.pk})