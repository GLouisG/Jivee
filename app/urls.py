from django.conf.urls import url
from .import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
urlpatterns=[
#  url(r'^api/users$', views.UserApi.as_view(),name = "apiusers" ),
#  url(r'^api/profiles/$', views.ProfileApi.as_view(),name = "apiprofiles" ),
 path("api/ai/<str:params>", views.MusicApi1.as_view(), name="spotifysuggest"),   
 path("api/deezerai/<str:musician>/<str:songname>", views.DeezerRecommendation.as_view(), name="deezersuggest"),  
]