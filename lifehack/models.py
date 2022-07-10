from random import randint
from django.db import models
import json


class User(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    points = models.IntegerField(default=0)
