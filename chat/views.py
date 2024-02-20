from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatRoom, Message
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import ChatRoomForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView


class ChatRoomCreateView(CreateView):
    model = ChatRoom
    form_class = ChatRoomForm
    template_name = 'chat/create_room.html'
    success_url = reverse_lazy('chat:room_list')  # Update with the correct URL name

    def get_form_kwargs(self):
        kwargs = super(ChatRoomCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    def form_valid(self, form):
        form.instance.save()
        form.instance.members.add(self.request.user)  # Add the creator as a member
        return super().form_valid(form)

class ChatRoomListView(ListView):
    model = ChatRoom
    template_name = 'chat/room_list.html'
    context_object_name = 'rooms'

@login_required
def join_chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    room.members.add(request.user)
    return redirect('chat:chat_room', room_id=room_id)  # Adjust with your actual chat room view

def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    # Fetch the last 50 messages in the room
    messages = Message.objects.filter(room=room).order_by('-timestamp')[:50]
    
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'messages': messages[::-1],  # Reverse messages to display in chronological order
    })