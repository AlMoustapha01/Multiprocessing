from rest_framework import serializers
from .models import Compte

class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = '__all__'

