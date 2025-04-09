import logging
from pymongo import MongoClient
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, LeaderboardSerializer, WorkoutSerializer
from .models import User, Team, Activity, Leaderboard, Workout

logger = logging.getLogger(__name__)

@api_view(['GET'])
def api_root(request, format=None):
    base_url = 'https://friendly-succotash-jj7xj6rw7979hpwqg-8000.app.github.dev/'
    return Response({
        'users': base_url + 'api/users/?format=api',
        'teams': base_url + 'api/teams/?format=api',
        'activities': base_url + 'api/activities/?format=api',
        'leaderboard': base_url + 'api/leaderboard/?format=api',
        'workouts': base_url + 'api/workouts/?format=api'
    })

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        users = list(db.users.find())
        for user in users:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return Response(users)

class TeamViewSet(viewsets.ViewSet):
    def list(self, request):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        teams = list(db.teams.find())
        for team in teams:
            team['_id'] = str(team['_id'])  # Convert ObjectId to string
            if 'members' in team:
                team['members'] = [str(member) for member in team['members']]  # Convert ObjectId in members to string
        return Response(teams)

class ActivityViewSet(viewsets.ViewSet):
    def list(self, request):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        activities = list(db.activity.find())
        for activity in activities:
            activity['_id'] = str(activity['_id'])  # Convert ObjectId to string
            activity['user'] = str(activity['user'])  # Convert ObjectId in user to string
        return Response(activities)

class LeaderboardViewSet(viewsets.ViewSet):
    def list(self, request):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        leaderboard = list(db.leaderboard.find())
        for entry in leaderboard:
            entry['_id'] = str(entry['_id'])  # Convert ObjectId to string
            entry['user'] = str(entry['user'])  # Convert ObjectId in user to string
        return Response(leaderboard)

class WorkoutViewSet(viewsets.ViewSet):
    def list(self, request):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        workouts = list(db.workouts.find())
        for workout in workouts:
            workout['_id'] = str(workout['_id'])  # Convert ObjectId to string
        return Response(workouts)
