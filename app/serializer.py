from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = [Profile]
        fields = ('id','current_playlist','credentials2', 'description', 'credentials1', 'pic') 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')