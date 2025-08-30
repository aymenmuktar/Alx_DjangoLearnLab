from django.urls import path
from .views import (RegisterView, LoginView, ProfileView,MeView, FollowUserView, UnfollowUserView,
    FollowingListView, FollowersListView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
     path("me/", MeView.as_view(), name="me"),

    # Follow / unfollow actions
    path("follow/<int:user_id>/", FollowUserView.as_view(), name="follow-user"),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view(), name="unfollow-user"),

    # Followers / following lists
    path("<int:user_id>/following/", FollowingListView.as_view(), name="user-following"),
    path("<int:user_id>/followers/", FollowersListView.as_view(), name="user-followers"),
    path("following/", FollowingListView.as_view(), name="me-following"),
    path("followers/", FollowersListView.as_view(), name="me-followers"),
]

