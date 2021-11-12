from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd                                                       
from sklearn import preprocessing                              
from sklearn.neighbors import KNeighborsClassifier                       
import numpy as np 

# Create your views here.
