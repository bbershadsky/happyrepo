import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils import timezone
from rest_framework.authtoken.models import Token
from datetime import date

class Team(models.Model):
    team_name = models.CharField(blank=True, max_length=200, null=True)

    def __str__(self):
        return str(self.team_name)

class User(AbstractUser):
    """Custom User extends Django Default, includes Team"""
    team = models.ForeignKey(Team, related_name="team", blank=True, null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)

class Rating(models.Model):
    rating_score = models.IntegerField(blank=True, default=5) # 1 to 5
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    date = models.DateField(blank=False, default=date.today)

    def __str__(self):
        return str(self.user) + " | " + str(self.rating_score)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create User token"""
    if created:
        Token.objects.create(user=instance)
