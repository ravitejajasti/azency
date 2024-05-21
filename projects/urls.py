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

# from django.urls import path
# from .views import (
#     ProjectListCreateAPIView,
#     ProjectRetrieveUpdateAPIView,
#     TaskListCreateAPIView,
#     TaskRetrieveUpdateDestroyAPIView,
#     SectionTaskListAPIView,
#     CommentListCreateAPIView,
# )

# urlpatterns = [
#     path('', ProjectListCreateAPIView.as_view(), name='project_list'),
#     path('new/', ProjectListCreateAPIView.as_view(), name='project_create'),
#     path('<int:pk>/', ProjectRetrieveUpdateAPIView.as_view(), name='project_detail'),
#     path('<int:pk>/edit/', ProjectRetrieveUpdateAPIView.as_view(), name='project_edit'),
#     path('<int:project_id>/tasks/', TaskListCreateAPIView.as_view(), name='task_list'),
#     path('<int:project_id>/tasks/new', TaskListCreateAPIView.as_view(), name='task_create'),
#     path('<int:project_id>/tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task_detail'),
#     path('tasks/<int:pk>/edit/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task_edit'),
#     path('<int:project_id>/sections/tasks/', SectionTaskListAPIView.as_view(), name='section_task_list'),
#     path('<int:project_id>/tasks/<int:pk>/comments/', CommentListCreateAPIView.as_view(), name='comment_list_create'),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#### API URLs

from django.urls import path
from .views import TaskDeleteAPIView

urlpatterns += [
    # your other URL patterns...
    path('api/projects/<int:project_id>/tasks/<int:task_id>/delete/', TaskDeleteAPIView.as_view(), name='task-delete-api'),
]
