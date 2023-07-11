from django import forms
from .models import Chatbox, Poll, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_id', 'text', 'chatbox_id']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title, option_a_label, option_b_label, creator, chatbox, duration_minutes']
        
class ChatboxForm(forms.ModelForm):
    class Meta:
        model = Chatbox
        fields = ['chatbox_id']