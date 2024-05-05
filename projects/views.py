from django.views.generic import ListView
from .models import Project, Task, Section
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from .forms import TaskForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

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
    model = Section
    context_object_name = 'sections'
    template_name = 'projects/task_list.html'

    def get_queryset(self):
        return Section.objects.filter(project_id=self.kwargs['project_id']).prefetch_related('tasks')
        #Task.objects.filter(project_id=self.kwargs['project_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])

        return context
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()  # Or filter as per your requirements
        self.object_list = self.get_queryset()  # Utilize the customized queryset
        context = self.get_context_data()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle AJAX request; return only the partial content
            return render(request, 'projects/partials/task_list.html', context)
        
        # Handle regular request; return the full page
        return render(request, 'projects/task_list.html', context)

class TaskDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'projects/task_detail.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        # Ensure we're passing instance to the form to populate it with existing values
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object  # Here, 'self.object' is the Task instance being detailed
        if hasattr(self.object, 'project_id'):
            kwargs['project_id'] = self.object.project_id
        return kwargs

    def post(self, request, *args, **kwargs):
        # This is necessary to handle post requests
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'success': True,
                'redirect_url': self.get_success_url(),
                'message': 'Task updated successfully.',
                'pk': self.kwargs.get('pk'),
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400, safe=False)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        # Redirects after a successful update
        return reverse_lazy('task_detail', kwargs={'project_id': self.object.project.id, 'pk': self.object.pk})
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data(form=form)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'projects/partials/task_form.html', context)
        return render(request, self.template_name, context)
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'projects/partials/task_form.html'
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
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'success': True,
                'redirect_url': self.get_success_url(),
                'message': f'Task created successfully. ',
                'pk': self.object.pk
            }
            return JsonResponse(data)
        else:
            return response
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400, safe=False)
        return super().form_invalid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    #fields = ['title', 'description', 'status', 'due_date', 'assigned_to', 'parent', 'section']
    form_class = TaskForm
    template_name = 'projects/task_form.html'


    def get_form_kwargs(self):
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs['project_id'] = self.object.project_id
        return kwargs

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        response = super(TaskUpdateView, self).form_valid(form)
        # Manually check for the 'X-Requested-With' header to identify AJAX requests
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'success': True,
                'redirect_url': self.get_success_url(),
                'message': f'Task updated successfully. ',
                'pk': self.kwargs.get('pk')
            }
            return JsonResponse(data)
        else:
            return response
            
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400, safe=False)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'project_id': self.object.project.id, 'pk': self.object.pk})
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data(form=form)
        # Render the partial page for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'projects/partials/task_form.html', context)
        # Render the full page for non-AJAX requests
        return render(request, 'projects/partials/task_form.html', context)
    
from rest_framework.generics import ListAPIView
from .serializers import ProjectSerializer, TaskSerializer

class ProjectListAPIView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskListAPIView(ListAPIView):
    queryset = Task.objects.all().select_related('project')  # Improve performance

    serializer_class = TaskSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Task.objects.filter(project_id=project_id)
