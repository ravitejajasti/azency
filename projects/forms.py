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
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contract Follow-up', 'label': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Follow-up with James and his team about the Contract'}),
            'due_date': forms.DateInput(attrs={'class': 'js-flatpickr form-control flatpickr-custom', 'placeholder':"Select dates", 'data-hs-flatpickr-options':'{"dateFormat": "Y-m-d"}'}),
            'assigned_to': forms.Select(attrs={'class': 'js-select form-control', 'data-hs-tom-select-options':'{"placeholder": "Select a person..."}'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        project_id = kwargs.pop('project_id', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False  # Explicitly set required to False

        if project_id:
            self.fields['assigned_to'].queryset = User.objects.filter(projects_joined=project_id)
        else:
            self.fields['assigned_to'].queryset = User.objects.none()