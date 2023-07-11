from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Poll, Comment, Chatbox, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('metamask_wallet_address',)
        
class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'userprofile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('userprofile')
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password is not None:
            user.set_password(password)
        user.is_staff = True
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    creator_name = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'creator', 'creator_name', 'text', 'created_at', 'chatbox']

class ChatboxSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chatbox
        fields = ['chatbox_id', 'comments']

class PollSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()
    percentages = serializers.SerializerMethodField()
    voting_status = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super(PollSerializer, self).create(validated_data)

    def get_user(self, obj):
        return obj.creator.username

    def get_total_votes(self, obj):
        return obj.get_total_votes()

    def get_percentages(self, obj):
        return obj.get_percentage()

    def get_voting_status(self, obj):
        obj.update_voting_status()
        return obj.voting_status
