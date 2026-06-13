from django.db import models
from rest_framework import viewsets
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializers, RegisterSerializers
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers

