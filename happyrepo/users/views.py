from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from .models import User, Rating
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateUserSerializer, UserSerializer, RatingSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from .permissions import IsUserOrReadOnly

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)

class UserSubmitSet(viewsets.ModelViewSet):
    """
    Submit a happiness level rating between 1-5
    """
    queryset = Rating.objects.all().order_by('-id')
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HappinessView(APIView):
    """
    Return the statistics of user's team - the number of people at each level of happiness
    Return average happiness of the user's team
    """
    def get(self, request, format=None):
        user = request.auth
        if user is not None:
            # Find all ratings in this user's team
            user = request.user
            rating5 = Rating.objects.filter(user__team=user.team, rating_score=5).count()
            rating4 = Rating.objects.filter(user__team=user.team, rating_score=4).count()
            rating3 = Rating.objects.filter(user__team=user.team, rating_score=3).count()
            rating2 = Rating.objects.filter(user__team=user.team, rating_score=2).count()
            rating1 = Rating.objects.filter(user__team=user.team, rating_score=1).count()
            ratings = Rating.objects.filter(user__team=user.team)
            team_avg = ratings.aggregate(Avg('rating_score')) # Take the average
            try: # Handle empty database
                team_averages = round(team_avg['rating_score__avg'],2)
            except:
                team_averages = 0

            content = {
                'user': str(request.user),
                'user\'s_team': str(user.team),
                '*': rating1,
                "**": rating2,
                "***": rating3,
                "****": rating4,
                "*****": rating5,
                "team_averages": team_averages,
            }
        else:
            ratings = Rating.objects.all()
            try:
                team_avg = ratings.aggregate(Avg('rating_score')) # Take the average
                team_avg = round(team_avg['rating_score__avg'],2)
            except:
                team_avg = 0
            content = {
                'Team Average Happiness': team_avg
            }
        return Response(content)

class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)
