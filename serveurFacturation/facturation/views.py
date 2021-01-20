from django.shortcuts import redirect, render
from rest_framework import response
from .models import Ordre
from .serializers import OrdreSerializer
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
import requests
# Create your views here.

class OrdreView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= OrdreSerializer
    queryset = Ordre.objects.all()
    lookup_field='id'

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class OrdreViewById(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= OrdreSerializer
    queryset = Ordre.objects.all()

    lookup_field='id'

    def get(self,request,id=None):
        return self.retrieve(request)
    
    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id=None):
        return self.destroy(request,id)

def banque(telephone):
    url ='http://localhost:4000/api/comptes/telephone/'+str(telephone)
    response= requests.get(url)
    data= response.json()
    return data

from rest_framework.decorators import api_view
@api_view(['GET', 'POST'])
def verification_banque(request):
    """
    List all code snippets, or create a new snippet.
    """
   
    if request.method == 'POST':
        data= request.data
        telephone=data['telephone']
        banq = banque(telephone)
        if data['total']>banq['solde']:

            return Response({'status':'impossible'})
        else:
            solde= banq['solde']-data['total']
            url ='http://localhost:4000/api/comptes/telephone/'+str(telephone)
            achat = requests.put(url,{'nom':banq['nom'],'prenom':banq['prenom'],'email':banq['email'],'telephone':banq['telephone'],'solde':solde})
            return Response({'status':'possible'})