from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import mixins,views
from rest_framework import generics
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .models import Ordre
from .serializers import OrdreSerializer
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import pika
import json 
import datetime
import requests
from django.conf import settings
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
def login_view(request): 
    # create a dictionary to pass
    if (request.POST):
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("/stocks") 
        else:
            error="Le nom d'utilisateur ou me mot de passe est incorrect"
            # Return an 'invalid login' error message.
            return render(request, "login/login.html",{'error':error}) 
    return render(request, "login/login.html") 

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect("/login")

def register_view(request): 
    # create a dictionary to pass 
    # data to the template 
    if request.method == "POST":
        if request.POST['pass'] != request.POST['passconf']:
            confError = "La confirmation du mot de passe a échoué"
            return render(request, "login/register.html",{'error': confError}) 
        elif len(request.POST['pass'])<8:
            lenghtError = "Mot de passe trop court"
            return render(request, "login/register.html",{'error': lenghtError}) 
        else:
            user = User()
            user.username = request.POST['username']
            user.password = request.POST['pass']
            user.save()
            return render(request, "login/register.html",{'success': "Le compte a bien été crée"})
    # return response with template and context 
    return render(request, "login/register.html") 

def all_commande():
    url= "http://127.0.0.1:7000/api/commandes"
    response = requests.get(url)
    data= response.json()
    if response.status_code == 200:
        return data
    else:
        return None

def article_by_id(id):
    print(id)
    url = "http://127.0.0.1:8000/api/articles/"+str(id)
    response = requests.get(url)
    print(response.status_code)
    data= response.json()
    article={
        'intitule': data['intitule'],
        'quantite': data['quantite'],
    }
    return article

def user_by_id(id):
     url= "http://127.0.0.1:7000/api/users/"+str(id)
     response = requests.get(url)
     data= response.json()
     user={
         'nom': data['first_name'],
         'prenom':data['last_name'],
         'email': data['email']
     }
     return user
def total(prix,quantity):
    montant = int(prix.replace(' ',''))
    return montant*quantity
def commande_view(request):
    
    data= all_commande()
    big_data=[]
    for elt in data:
        user= user_by_id(elt['user'])
        article= article_by_id(elt['produit'])
        stocks=article['quantite']>elt['quantite']

        #verification = requests.post("http://127.0.0.1:3000/api/verification/",{'telephone':elt['telephone'],'total':total(elt['prix'],elt['quantite'])})
        
        small={
            'nom':user['nom'],
            'prenom':user['prenom'],
            'intitule':article['intitule'],
            'prix':elt['prix'],
            'quantite':elt['quantite'],
            'date':elt['date_add'],
            'telephone':elt['telephone'],
            'stock': stocks,
            'verification':'possible'
        }
        ordre= Ordre()
        ordre.nom=user['nom']
        ordre.prenom = user['prenom']
        ordre.prix=elt['prix']
        ordre.telephone=elt['telephone']
        ordre.total= total(elt['prix'],elt['quantite'])
        ordre.produit=article['intitule']
        ordre.save()

        big_data.append(small)
    print(big_data)
    return render(request,"clientele/base.html",{'data':big_data})
