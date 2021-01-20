from rest_framework import serializers
from .models import Panier,Commande
from django.contrib.auth.models import User
class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'