from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd                                                       
from sklearn import preprocessing                              
from sklearn.neighbors import KNeighborsClassifier                       
import numpy as np 
from app.serializer import *
from django.contrib.auth.models import User
# Create your views here.

class ProfileApi(APIView):
    def get(self, request, format=None):
        profs = Profile.objects.all()
        serializers = ProfileSerializer(profs, many=True)
        return Response(serializers.data)   

class UserApi(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializers = ProfileSerializer(users, many=True)
        return Response(serializers.data)       