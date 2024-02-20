# forms.py in your chat app

from django import forms
from django.contrib.auth import get_user_model
from .models import ChatRoom

User = get_user_model()

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'members']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the current user from view kwargs
        super(ChatRoomForm, self).__init__(*args, **kwargs)
        if self.user:  # Exclude the current user from the members queryset
            self.fields['members'].queryset = User.objects.exclude(pk=self.user.pk)