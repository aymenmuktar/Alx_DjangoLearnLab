from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from .models import CustomUser
from posts.models import Post
from .serializers import PostSerializer
from django.contrib.auth import authenticate
from .serializers import PostSerializer,RegisterSerializer, UserSerializer,MeSerializer,PublicUserSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from notifications.utils import create_notification

User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            target_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=404)

        request.user.following.add(target_user)
        create_notification(
            recipient=target_user,
            actor=request.user,
            verb="followed you"
        )
        return Response({'detail': f'You are now following {target_user.username}'})

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        try:
            request.user.unfollow(target_user)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"user": UserSerializer(user).data, "token": token.key}, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data["username"])
        token = Token.objects.get(user=user)
        return Response({"user": response.data, "token": token.key})

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid Credentials"}, status=400)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class FeedPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = [permissions.AllowAny]


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_qs = request.user.following.all().values_list("pk", flat=True)
        qs = (
            Post.objects
            .filter(author_id__in=following_qs)
            .select_related("author")
            .order_by("-created_at", "-id")
        )

        paginator = FeedPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = PostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
