from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('new/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('<int:project_id>/tasks/', TaskListView.as_view(), name='task_list'),
    path('<int:project_id>/tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:project_id>/tasks/new/', TaskCreateView.as_view(), name='task_create'),
    path('<int:project_id>/tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from .views import ProjectListAPIView, TaskListAPIView

urlpatterns += [
    path('api/projects/', ProjectListAPIView.as_view(), name='api_project_list'),
    path('api/tasks/<int:project_id>/', TaskListAPIView.as_view(), name='api_task_list'),
]
