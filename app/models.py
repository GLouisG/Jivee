from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  pic = models.ImageField(upload_to = 'hood/', default='profpic.jpg')
  description = models.TextField(default='Welcome')
  credentials1 = models.TextField(blank=True)
  credentials2 = models.TextField(blank=True) 
  current_playlist = models.CharField(max_length=250, blank=True)
  
  def __str__(self):
            return f'Profile {self.description}'   
  @classmethod
  def get_profile(cls, id):
      object = cls.objects.get(id=id)
      return object
