from rest_framework import serializers
from authentication.models import User
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from authentication.tasks import send_email
import re
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt




class RegisterSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    username=serializers.CharField()
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')

        if not re.match(r'^[^\d\W_]+( [^\d\W_]+)*$', username.strip(), re.UNICODE):
            raise serializers.ValidationError(
                'The Name should only contain letters'
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'This Email is already used'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'this Name is already used'
            )
        return attrs

    
    def create(self, validated_data):
        request=self.context.get('request')
        user = User.objects.create_user(**validated_data)
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+'?token='+str(token)
        email_body = 'Use this link below to verify your Email \n\n'+absurl
        data = {'email_body': email_body, 'to_email':user.email,
                'email_subject': 'Verify your Email'}

        send_email.delay(data)
        return user
    

class EmailVerificationSerializer(serializers.Serializer):

    def validate(self, attrs):

        request=self.context.get('request')
        token = request.GET.get('token')       
        try:

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.email_is_verified:
                user.email_is_verified = True
                user.save()

            if user.email_is_verified and user.phonenumber_is_verified:
                user.is_verified = True
                user.save()

        except jwt.ExpiredSignatureError as identifier:
            
            raise AuthenticationFailed("Activation expired")
        
        except jwt.exceptions.DecodeError as identifier:
            
            raise AuthenticationFailed('Invalid token')
        return attrs 