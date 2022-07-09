from django.http import HttpResponse, JsonResponse
from .models import User, Bin
from .serializers import UserSerializer, BinSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def home_view(*args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")


@api_view(['GET', 'POST', 'PUT'])
def user_info(request):

    if request.method == 'GET':
        try:
            user = User.objects.get(pk=request.data["name"])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            user = User.objects.get(pk=request.data["name"])
        except User.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            user = User.objects.get(pk=request.data["name"])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status =status.HTTP_404_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'PUT'])
def bin_info(request):

    if request.method == 'GET':
        try:
            bin = Bin.objects.get(pk=request.data["name"])
        except Bin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BinSerializer(bin)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            bin = Bin.objects.get(pk=request.data["name"])
        except Bin.DoesNotExist:
            serializer = BinSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            bin = Bin.objects.get(pk=request.data["name"])
        except Bin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BinSerializer(bin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status =status.HTTP_404_BAD_REQUEST)
