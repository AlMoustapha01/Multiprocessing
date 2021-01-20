# Generated by Django 3.0.5 on 2021-01-18 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('prix', models.CharField(blank=True, max_length=255, null=True)),
                ('quantite', models.IntegerField(blank=True, null=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'panier',
                'managed': 'True',
            },
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produit', models.IntegerField(blank=True, null=True)),
                ('telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('localisation', models.CharField(blank=True, max_length=255, null=True)),
                ('prix', models.CharField(blank=True, max_length=255, null=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
