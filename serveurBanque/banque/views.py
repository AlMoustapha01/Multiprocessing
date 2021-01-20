from django.shortcuts import redirect, render
from .models import Compte
from .serializers import CompteSerializer
from rest_framework.response import Response
from rest_framework import mixins,views
from rest_framework import generics
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import pika
import json 
import datetime
# Create your views here.

class CompteView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= CompteSerializer
    queryset = Compte.objects.all()
    lookup_field='id'

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class CompteViewById(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= CompteSerializer
    queryset = Compte.objects.all()

    lookup_field='id'

    def get(self,request,id=None):
        return self.retrieve(request)
    
    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id=None):
        return self.destroy(request,id)

class CompteViewByTelephone(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= CompteSerializer
    queryset = Compte.objects.all()

    lookup_field= "telephone"

    def get(self,request,telephone=None):
        return self.retrieve(request)
    
    def put(self,request,telephone=None):
        return self.update(request,telephone)

    def delete(self,request,telephone=None):
        return self.destroy(request,telephone)