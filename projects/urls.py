from django.urls import path
from .views import (
    ProjectListCreateAPIView,
    ProjectRetrieveUpdateAPIView,
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    SectionTaskListAPIView,
    CommentListCreateAPIView,
    SectionListCreateAPIView,
    SectionRetrieveUpdateDestroyAPIView,
    TaskDeleteAPIView,
    ProjectDetailAPIView
)

app_name = 'projects'

urlpatterns = [
    path('', ProjectListCreateAPIView.as_view(), name='project_list'),
    path('new/', ProjectListCreateAPIView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectRetrieveUpdateAPIView.as_view(), name='project_detail'),
    path('<int:pk>/edit/', ProjectRetrieveUpdateAPIView.as_view(), name='project_edit'),
    path('<int:project_id>/tasks/', TaskListCreateAPIView.as_view(), name='task_list'),
    path('<int:project_id>/tasks/new', TaskListCreateAPIView.as_view(), name='task_create'),
    path('<int:project_id>/tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task_edit'),
    path('<int:project_id>/sections/tasks/', SectionTaskListAPIView.as_view(), name='section_task_list'),
    path('<int:project_id>/tasks/<int:pk>/comments/', CommentListCreateAPIView.as_view(), name='comment_list_create'),

    # Section endpoints
    path('<int:project_id>/sections/', SectionListCreateAPIView.as_view(), name='section-list-create'),
    path('<int:project_id>/sections/<int:pk>/', SectionRetrieveUpdateDestroyAPIView.as_view(), name='section-retrieve-update-destroy'),
    
    # API URL for task deletion
    path('api/projects/<int:project_id>/tasks/<int:task_id>/delete/', TaskDeleteAPIView.as_view(), name='task-delete-api'),

     # New project detail API
    path('<int:pk>/detail/', ProjectDetailAPIView.as_view(), name='project-detail-api'),
]
