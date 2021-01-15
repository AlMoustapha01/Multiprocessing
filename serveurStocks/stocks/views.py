from django.shortcuts import redirect, render
from .models import Article
from .serializers import ArticleSerializer
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

from django.conf import settings
# Create your views here.
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

@login_required(login_url='/login')
def stocks_view(request): 
    # create a dictionary to pass 
    # data to the template 
    stock = list(Article.objects.values())
    # return response with template and context 
    return render(request, "stocks/base.html", {'data':stock})
 
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
def refresh(request):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_HOST))  
    channel = connection.channel()
    channel.queue_declare(queue=settings.QUEUE_TOPIC)
    article = list(Article.objects.values())
    print(article)

    message = json.dumps(article)
    channel.basic_publish(exchange='', routing_key=settings.QUEUE_TOPIC, body=article) 

    print(" [x] Sent data to RabbitMQ") 

    connection.close()
    return render(request, "stocks/base.html", {'data':message})  
class ArticleView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= ArticleSerializer
    queryset = Article.objects.all()
    lookup_field='id'

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class ArticleViewById(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class= ArticleSerializer
    queryset = Article.objects.all()

    lookup_field='id'

    def get(self,request,id=None):
        return self.retrieve(request)
    
    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id=None):
        return self.destroy(request,id)