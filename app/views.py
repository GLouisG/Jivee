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
from . import suggestion
import json
import codecs
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

# class MusicApi1(APIView):
#   #for spotify
#     def get(self, request, *args, **kwargs):
#         query = kwargs.get('params', None)
#         response = requests.get('https://agrofake.herokuapp.com/api/ai/'+query)
#         json_without_slash = response.json()

#         return Response(json_without_slash) 

class MusicApi1(APIView):
  #for spotify
    def get(self, request, *args, **kwargs):
        query = self.kwargs.get('params', None)
        query = query.replace("%20", " ")
        res = suggestion.suggester(query)
        resp = "[{'track_name':'Sorry', 'artist_name':'We were unable to find your playlist on spotify, ensure it exists and is public', 'url':'https://static.wikia.nocookie.net/g-idle/images/6/6c/Uh-Oh_%28Album_Cover%29.jpg/revision/latest?cb=20190626170027', 'genre':'Try again'}]"


        resp = json.dumps(resp)
        resp = json.loads(resp)
        print(res)
        if "Error" in res:
            return Response({'songs': resp})
        else:
            return Response({'songs':res}) 

class MusicApi2(APIView):
  #for 2nd service
    def get(self, request, *args, **kwargs):
        musician = kwargs.get('musician', None)
        songname  = kwargs.get("songname", None)
        response = requests.get('https://deezerapi123.herokuapp.com/api/ai/' +musician+ "/"+songname)
        json_without_slash = response.json()

        return Response(json_without_slash)    



