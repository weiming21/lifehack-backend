from email.policy import default
from tempfile import NamedTemporaryFile
from tokenize import Name
from django.http import HttpResponse, JsonResponse
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import PIL.Image as Image
import io
import os
from .utils import *
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


import cloudinary
import cloudinary.uploader
import cloudinary.api


def home_view(*args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")


@api_view(["POST", "PUT"])
def user_info(request):
    try:
        user = User.objects.get(pk=request.data["name"])
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


@api_view(["POST"])
def new_user(request):
    if request.method == "POST":
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


@api_view(["PUT"])
def classify_image(request):
    data = {'success': False}
    url = ''

    if request.method == "PUT":
        if request.FILES.get("image", None) is not None:
            image_request = request.FILES["image"]
            image_bytes = image_request.read()
            image = Image.open(io.BytesIO(image_bytes))

            tmp_plot1 = NamedTemporaryFile()
            image.save(tmp_plot1.name + ".png")
            tmp_plot1.close()

            processed_image = inference(image)
            tmp_plot2 = NamedTemporaryFile()
            processed_image.save(tmp_plot2.name + ".png")

        try:
            original_image_response = cloudinary.uploader.upload(
                tmp_plot1.name + ".png")
            processed_image_response = cloudinary.uploader.upload(
                tmp_plot2.name + ".png")
        except:
            original_image_response = {'url': ''}
            processed_image_response = {'url': ''}
        # print(original_image_response)
        # print(processed_image_response)
        tmp_plot2.close()

        data['original_image_url'] = original_image_response["url"]
        data['processed_image_url'] = processed_image_response["url"]
        return JsonResponse(data)
