from django.db import models

# Create your models here.
class Article(models.Model):
    intitule= models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True)
    prix = models.CharField(max_length=255, blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        managed= 'True'
        db_table = 'article'