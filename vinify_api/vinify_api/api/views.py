from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.contrib.auth import get_user_model
User=get_user_model()
import six
import sys
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser,MultiPartParser,FormParser,JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status




from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MyUserSerializer, MyUserChangeSerializer


class MyUserMe(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyUserSerializer

    def get(self, request, format=None):
        return Response(self.serializer_class(request.user).data)


class MyUserMeChange(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyUserChangeSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            fields=user._meta.fields ## should be only fields tha may be changed , otherwise won't be secure
            for key in fields:
                if key in serializer.data:
                    setattr(user,key,serializer.data[key])
            user.save()

            content = {'success': _('User information changed.')}
            return Response(content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Get_recomendations(APIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = MyUserChangeSerializer
    def get(self, request, format=None):
        data={"data":get_nearest(point_to_check=[float(request.GET.get("boldness")),float(request.GET.get("acidity"))],wbesite_url=request.GET.get("wbesite_url"))} #
        return Response(data)

class MyUserMeChange(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WineSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            fields=user._meta.fields
            for key in fields:
                if key in serializer.data:
                    setattr(user,key,serializer.data[key])
            user.save()

            content = {'success': _('User information changed.')}
            return Response(content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from scipy.spatial import KDTree

import numpy
def get_nearest(point_to_check,wine_data=None,wbesite_url=None):
    from api.models import wine
    wine_data1=wine_data if wine_data else wine.objects.all().filter(wine_boldness__isnull=False,wine_acidity__isnull=False).values_list("wine_boldness","wine_acidity","wine_url")
    wine_data1=wine_data1.filter(website__url__icontains=wbesite_url) if wbesite_url else wine_data1
    wine_data=numpy.array([numpy.array(xi[:2]) for xi in wine_data1 if xi ])
    """v =wine_data# np.random.rand(n, 3)
    kdtree = KDTree(v)
    d, i = kdtree.query((point_to_check))
    print("closest point:", v[i])"""
    target_point =point_to_check
    wines_sorted=sorted([numpy.array(xi) for xi in wine_data  ],key=lambda point:distance_squared(target_point[0],target_point[1],*point))
    for i,wine in enumerate(wines_sorted[:5]) :
        for wine_n in wine_data1:
            if wine_n[0]==wine[0] and wine_n[1]==wine[1]:

                wines_sorted[i]=numpy.array(wine_n)
                break
    return wines_sorted[:5]

def distance_squared(x1,y1,x2,y2):
    return (x1-x2)**2 + (y1-y2)**2


