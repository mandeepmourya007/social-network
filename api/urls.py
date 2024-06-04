from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView, CustomAuthToken, UserSearchView, FriendRequestView, FriendListView, PendingFriendRequestsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/<int:pk>/', FriendRequestView.as_view(), name='friend-request-respond'),
    path('friends/', FriendListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
]
