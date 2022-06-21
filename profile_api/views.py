from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profile_api import permissions
from profile_api import models, seriliazers

class HellowApiView(APIView):
   serializer_class = seriliazers.HellowSerializer
   def get(self, request, format=None):
      response_list = [
         'This is the first response',
         'This is the second response',
         'this is the third response'
      ]
      return Response({'response':response_list})
   
   def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
         name = serializer.validated_data.get('name')
         age = serializer._validated_data.get('age')
         message = f'Good morning, my name is Mr {name}, I am {age} years old'
         return Response({'message':message})
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      
class HelloViewSet(ViewSet):
   serializer_class = seriliazers.HellowSerializer
   def list(self, request):
      names = [
         'Valery Guhena', 'Emmanuel Bouabre', 'Sery Luc', 'Bahi Charles'
      ]
      return Response(names)
   
   def create(self,request):
      serializer= self.serializer_class(data=request.data)
      
      if serializer.is_valid():
         name = serializer.validated_data.get('name')
         age = serializer.validated_data.get('age')
         message = f'This is {name}. He is {age} year old'
         return Response(message)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
class UserProfileViewSet(ModelViewSet):
   serializer_class = seriliazers.UserProfileSerializer
   queryset = models.UserProfile.objects.all()
   authentication_classes= (TokenAuthentication,)
   permission_classes =(permissions.UpdateOwnProfile,)
   filter_backends= (filters.SearchFilter),
   search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
   
class UserProfileFeedViewSet(ModelViewSet):
   authentication_classes= (TokenAuthentication,)
   serializer_class = seriliazers.ProfileItemFeedSerializer
   queryset = models.ProfileFeetItem.objects.all()
   permission_classes =(
      permissions.UpdateOwnFeed,
      IsAuthenticated
   )
   
   def perform_create(self, serializer): 
      serializer.save(user_profile = self.request.user)
      