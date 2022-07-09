from random import randint
from django.db import models
import json


class User(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    points = models.IntegerField(default=0)

class Bin(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    current = models.FloatField(default=0)


f = open('busstop.json')
# Read the JSON
titles = json.load(f)
# Create a Django model object for each object in the JSON 
for title in titles:
    b = Bin(name=title['Description'], latitude = title['Latitude'], longitude = title['Longitude'], current = randint(0, 100))
    b.save()