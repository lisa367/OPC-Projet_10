from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.http import Http404

from .serializers import UserSerializer
from .models import CustomUserModel


class SignupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response("Welcome to the SoftDesk API")

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        # print(serializer)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        if serializer.is_valid():
            print("Ok data")
            # print(f"Serializer : \n {serializer.data}")
            serializer.save()
            # print(final)
            # return Response(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"Sorry, didn't work : {request.data}", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        body = request.data
        id = body.get("id", None)
        if id:
            user = CustomUserModel.objects.filter(pk=id)
            if user:
                user[0].delete()
                return Response("User deleted")
            else:
                return Response("That id does not exists.")
            
    def put(self, request, *args, **kwargs):
        body = request.data
        new_password = body.get("password", 0)
        id = body.get("id", None)

        if id:
            user_entry = CustomUserModel.objects.filter(pk=id)
            if user_entry:
                user = user_entry[0]
                if new_password:
                    user.set_password(new_password)
                    user.save()
                    return Response("Password updated")
                else:
                    return Response("The password could not be updated.")
                
            else:
                return Response("That id does not exists.")
                
        else:
                return Response("No id was provided with the request.")
        pass