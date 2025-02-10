from django.shortcuts import render
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import *
# Create your views here.
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        if serializer.errors:
            print (serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)