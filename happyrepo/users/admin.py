from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Team, User, Rating


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'team', 'date_joined', 'is_staff',]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_name']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
Rating._meta.get_fields()]
