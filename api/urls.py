from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, CommentViewSet, ChatboxViewSet, UserCreate, CustomAuthToken

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'chatboxes', ChatboxViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserCreate.as_view(), name='user-register'),
    path('login/', CustomAuthToken.as_view(), name='user-login'),
    path('api-auth/', include('rest_framework.urls'))
    # Add /isTokenValid/
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Use this if you want to make all views require authentication by default
    ]
}