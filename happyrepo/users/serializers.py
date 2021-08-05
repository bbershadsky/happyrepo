# pylint: disable=too-few-public-methods
from rest_framework import serializers
from .models import User, Rating
from rest_framework.validators import UniqueTogetherValidator

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)
        read_only_fields = ('username', )

class RatingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Rating
        fields = ['rating_score', 'date', 'user']

        # Only 1 rating per user per day allowed
        validators = [
            UniqueTogetherValidator(
                queryset=Rating.objects.all(),
                fields=('user', 'date'),
                message=('You may only rate your happiness once per day')
            )
        ]

class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'auth_token',)
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}
