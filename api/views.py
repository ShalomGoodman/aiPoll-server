from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Poll, Comment, Chatbox
from .serializers import PollSerializer, CommentSerializer, ChatboxSerializer, UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated,]
        else:
            self.permission_classes = [AllowAny,]
        return super(PollViewSet, self).get_permissions()
    
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated,]
        else:
            self.permission_classes = [AllowAny,]
        return super(CommentViewSet, self).get_permissions()
        
    
    def perform_create(self, serializer):
        serializer.save()  
    
class ChatboxViewSet(viewsets.ModelViewSet):
    queryset = Chatbox.objects.all()
    serializer_class = ChatboxSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        comments = instance.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


