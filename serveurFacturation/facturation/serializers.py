from rest_framework import serializers
from .models import Ordre

class OrdreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordre
        fields = '__all__'

