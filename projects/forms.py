from django import forms
from .models import Task
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to', 'parent', 'section']  # Include 'parent'
        widgets = {
            # You can specify widgets here if needed
        }

    def __init__(self, *args, **kwargs):

        project_id = kwargs.pop('project_id', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False  # Explicitly set required to False

        if project_id:
            self.fields['assigned_to'].queryset = User.objects.filter(projects_joined=project_id)
        else:
            self.fields['assigned_to'].queryset = User.objects.none()