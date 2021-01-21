from django.db import models

# Create your models here.
class Ordre(models.Model):
    nom= models.CharField(max_length=255, blank=True, null=True)
    prenom= models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    telephone= models.CharField(max_length=255, blank=True, null=True)
    produit =  models.CharField(max_length=255, blank=True, null=True)
    prix =  models.IntegerField(blank=True, null=True)
    total=  models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        managed= 'True'
        db_table = 'ordre'