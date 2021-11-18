from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd                                                       
from sklearn import preprocessing                              
from sklearn.neighbors import KNeighborsClassifier                       
import numpy as np 
from app.serializer import *
import requests
import json
from django.contrib.auth.models import User
# Create your views here.

# class ProfileApi(APIView):
#     def get(self, request, format=None):
#         profs = Profile.objects.all()
#         serializers = ProfileSerializer(profs, many=True)
#         return Response(serializers.data)   

# class UserApi(APIView):
#     def get(self, request, format=None):
#         users = User.objects.all()
#         serializers = ProfileSerializer(users, many=True)
#         return Response(serializers.data)       

class MusicApi1(APIView):
  #for spotify
    def get(self, request, *args, **kwargs):
        query = kwargs.get('params', None)
        response = requests.get('https://agrofake.herokuapp.com/api/ai/'+query)
        json_without_slash = response.json()

        return Response(json_without_slash) 

class MusicApi2(APIView):
  #for 2nd service
    def get(self, request, *args, **kwargs):
        musician = kwargs.get('musician', None)
        songname  = kwargs.get("songname", None)
        response = requests.get('https://deezerapi123.herokuapp.com/api/ai/' +musician+ "/"+songname)
        json_without_slash = response.json()

        return Response(json_without_slash)    



