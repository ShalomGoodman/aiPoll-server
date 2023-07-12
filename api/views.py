from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.status import HTTP_200_OK
from .models import Poll, Comment, Chatbox
from .serializers import PollSerializer, CommentSerializer, ChatboxSerializer, UserSerializer
from rest_framework.decorators import action

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
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_winner()
        instance.update_voting_status()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        for instance in queryset:
            instance.update_winner()
            instance.update_voting_status()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        poll = self.get_object()
        option = request.data.get('option')
        if poll.voting_status == 'closed' or timezone.now() >= poll.deadline or poll.creator == request.user:
            return Response({'detail': 'You cannot vote.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if option == 'a':
                poll.option_a_votes += 1
            elif option == 'b':
                poll.option_b_votes += 1
            else:
                return Response({'detail': 'Invalid option.'}, status=status.HTTP_400_BAD_REQUEST)

            poll.update_winner()
            poll.update_voting_status()
            poll.save()

            return Response({'status': 'vote counted'})
    
    
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


