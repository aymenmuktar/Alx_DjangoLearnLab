from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from .models import Post, CustomUser
from .serializers import PostSerializer
from django.contrib.auth import authenticate
from .serializers import PostSerializer,RegisterSerializer, UserSerializer,MeSerializer,
    PublicUserSerializer,
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

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
