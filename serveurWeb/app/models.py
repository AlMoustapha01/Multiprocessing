from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Panier(models.Model):
    intitule= models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(null=True)
    prix = models.CharField(max_length=255, blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        managed= 'True'
        db_table = 'panier'

class Commande(models.Model):
    produit = models.IntegerField(blank=True, null=True)
    telephone= models.CharField(max_length=255, blank=True, null=True)
    localisation= models.CharField(max_length=255, blank=True, null=True)
    prix= models.CharField(max_length=255, blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now_add=True, blank=True)
