from rest_framework import serializers
from .models import User, Bin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "points"]

class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ["name", "longitude", "latitude", "current"]
