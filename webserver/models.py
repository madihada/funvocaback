from operator import mod
from pyexpat import model
from django.db import models

# Create your models here.
class Customer(models.Model):
    
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    info = models.CharField(max_length=200)

class Word(models.Model):
    
    name = models.CharField(max_length=200)
    info = models.CharField(max_length=200)