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

class MusicApi(APIView):
  #for spotify
    def get(self, request, format=None):

        return Response({"songs":[{"song1":"music"},{"song2":"music"}]}) #dummy response
class MusicApi2(APIView):
  #for 2nd service
    def get(self, request, format=None):

        return Response({"songs":[{"song1":"music"},{"song2":"music"}]}) #dummy response          