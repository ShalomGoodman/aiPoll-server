from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.status import HTTP_200_OK
from .models import Poll, Comment, Chatbox
from .serializers import PollSerializer, CommentSerializer, ChatboxSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    
    def perform_create(self, serializer):
        user = serializer.save()
        # Create a token for the new user and save it
        Token.objects.create(user=user)
        
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=HTTP_200_OK)

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


