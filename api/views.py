from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from .models import FriendRequest
from .serializers import UserSerializer, RegisterSerializer, FriendRequestSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


from django.db.models import Q


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q")
        if not query:
            return User.objects.none()

        filter_condition = (
            Q(email__iexact=query)
            | Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        return User.objects.filter(filter_condition)


class FriendRequestThrottle(UserRateThrottle):
    rate = "3/minute"


class FriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request):
        from_user = request.user
        to_user_id = request.data.get("to_user_id")
        to_user = User.objects.get(id=to_user_id)
        if from_user == to_user:
            return Response(
                {"error": "You cannot send a friend request to yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )
        if not created:
            return Response(
                {"error": "Friend request already sent."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        friend_request = FriendRequest.objects.get(id=pk)
        if friend_request.to_user != request.user:
            return Response(
                {"error": "You cannot respond to this friend request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        action = request.data.get("action")
        if action == "accept":
            friend_request.status = "accepted"
        elif action == "reject":
            friend_request.status = "rejected"
        else:
            return Response(
                {"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST
            )

        friend_request.save()
        return Response({"status": friend_request.status}, status=status.HTTP_200_OK)


class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        friends_from_user = FriendRequest.objects.filter(
            from_user=user, status="accepted"
        ).values_list("to_user", flat=True)
        friends_to_user = FriendRequest.objects.filter(
            to_user=user, status="accepted"
        ).values_list("from_user", flat=True)
        friends = friends_from_user.union(friends_to_user)

        return User.objects.filter(id__in=friends)


class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status="pending")
