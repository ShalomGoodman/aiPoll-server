from django.contrib import admin
from .models import Chatbox, Poll, Comment, UserProfile

admin.site.register(UserProfile)
admin.site.register(Chatbox)
admin.site.register(Poll)
admin.site.register(Comment)