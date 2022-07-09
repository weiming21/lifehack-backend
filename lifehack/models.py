from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    points = models.IntegerField(default=0)
