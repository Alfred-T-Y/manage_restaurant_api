from django.shortcuts import render
from rest_framework import generics, status, views
from authentication.serializers import (RegisterSerializer, 
    EmailVerificationSerializer,) #LoginSerializer, 
    #RequestPasswordResetEmailSerializer, SetNewPasswordSerializer,
    #PasswordTokenCheckAPISerializer, LogoutSerializer
from rest_framework.response import Response


# Create your views here.



class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
            context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        
        return Response(user_data, status=status.HTTP_201_CREATED)
    


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):

        serializer = self.serializer_class(data=request.data,
            context={'request':request})
        serializer.is_valid(raise_exception=True)
        
        return Response({'email': 'Sucessfully actived'}, status=status.HTTP_200_OK)