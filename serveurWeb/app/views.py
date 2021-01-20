from django.shortcuts import redirect, render
from .models import Commande,Panier
from .serializers import CommandeSerializer,PanierSerializer,UserSerializer
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

def all_article():
    response = requests.get("http://localhost:8000/api/articles")
    data= response.json()
    if response.status_code == 200:
        return data
    else:
        return None

def one_article(id):
    url = "http://localhost:8000/api/articles/"+str(id)
    response = requests.get(url)
    data= response.json()
    if response.status_code == 200:
        return data
    else:
        return None

def shop_view(request): 
    # create a dictionary to pass 
    # data to the template
    
    articles = all_article()
    # return response with template and context 
    return render(request, "shop.html", {'data':articles})


def detail_view(request,id): 
    # create a dictionary to pass 
    # data to the template
    article = one_article(id)
    
    # return response with template and context 
    return render(request, "detail.html", {'data':article})

def total(prix,quantity):
    montant = int(prix.replace(' ',''))
    return montant*quantity
@login_required(login_url='/login',redirect_field_name="next")
def panier_view(request):

    if(request.method=="POST"):
        if request.user.is_authenticated:
            produit= request.POST['produit']
            quantity = request.POST['quantity']
            article=one_article(produit)
            panier= Panier()
            panier.intitule = article['intitule']
            panier.image= article['image']
            panier.quantite = quantity
            panier.prix = article['prix']
            panier.user = request.user
            panier.save()
            
            
            return render(request, "cart.html", {'data':list(Panier.objects.filter(user=request.user))})
    print(request)
    return render(request, "cart.html", {'data':list(Panier.objects.filter(user=request.user))})

def commande_view(request):
    panier = Panier.objects.filter(user=request.user)
    if request.method == "POST":
        print("success success")
        nom=request.POST['nom']
        prenoms=request.POST['prenoms']
        email=request.POST['email']
        telephone=request.POST['telephone']
        produit=request.POST['produit']
        ville=request.POST['ville']
        commune= request.POST['commune']
        quartier=request.POST['quartier']
        localisation= ville+ ' '+ commune+' '+quartier
        unique = Panier.objects.get(pk=int(produit))
        prix= unique.prix
        user= User.objects.get(pk=request.user.id)
        user.first_name = nom
        user.last_name = prenoms
        user.email = email
        user.save()
        commande = Commande()
        commande.produit = produit
        commande.quantite= unique.quantite
        commande.telephone= telephone
        commande.localisation = localisation
        commande.prix= prix
        commande.user= request.user
        commande.save()
        success =" Bravo votre commande a bien été prise en compte"
        render(request, "checkout.html",{'data':panier,'success':success})
    return render(request, "checkout.html",{'data':panier})

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
            return redirect("/shop") 
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

class CommandeView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= CommandeSerializer
    queryset = Commande.objects.all()
    lookup_field='id'

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class CommandeViewById(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= CommandeSerializer
    queryset = Commande.objects.all()

    lookup_field='id'

    def get(self,request,id=None):
        return self.retrieve(request)
    
    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id=None):
        return self.destroy(request,id)


class PanierView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= PanierSerializer
    queryset = Panier.objects.all()
    lookup_field='id'

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class PanierViewById(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= PanierSerializer
    queryset = Panier.objects.all()

    lookup_field='id'

    def get(self,request,id=None):
        return self.retrieve(request)
    
    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id=None):
        return self.destroy(request,id)

class UserView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= UserSerializer
    queryset = User.objects.all()
    lookup_field='id'

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class UserViewById(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= UserSerializer
    queryset = User.objects.all()

    lookup_field='id'

    def get(self,request,id=None):
        return self.retrieve(request)
    
    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id=None):
        return self.destroy(request,id)