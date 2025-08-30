from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)

    def __str__(self):
        return self.username

    def follow(self, target):
        if target == self:
            raise ValueError("You cannot follow yourself.")
        target.followers.add(self)  # add self to target’s followers

    def unfollow(self, target):
        if target == self:
            raise ValueError("You cannot unfollow yourself.")
        target.followers.remove(self)

    def is_following(self, target) -> bool:
        return target.followers.filter(pk=self.pk).exists()

    def is_followed_by(self, user) -> bool:
        return self.followers.filter(pk=user.pk).exists()
