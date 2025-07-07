from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager,PermissionsMixin)
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumber_field.modelfields import PhoneNumberField
#from rest_framework_simplejwt.tokens import RefreshToken


def normalize_phone(phone):
    try:
        # On suppose que le numéro est au format international ou commence par +
        parsed = phonenumbers.parse(phone, None)  # Pas de région forcée

        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Phone number invalid.")

        # Retourne au format E.164 : +1234567890
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    
    except NumberParseException as e:
        raise ValueError("The phone number is in a invalid format") from e


class UserManager(BaseUserManager):

    def create_user(self, email, username, phonenumber ,password=None):
        
        if email is None:
            raise TypeError('The Email is required')
        if username is None:
            raise TypeError('The Name is required')
        if phonenumber is None:
            raise TypeError('The phone number is required')

        user = self.model(
            email=self.normalize_email(email),
            phonenumber=self.normalize_email(phonenumber),
            username=username
        )
        user.set_password("sal"+password+"age")
        user.save()
        return user

    def create_superuser(self, email, username, phonenumber, password=None):

        if password is None:
            raise TypeError('The Password is required')

        user = self.create_user(email, username, phonenumber, password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phonenumber = PhoneNumberField(unique=True, db_index=True, region=None)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phonenumber']  

    objects = UserManager()

    def __str__(self):
        return self.username

    """def tokens(self):
        tokens = RefreshToken.for_user(self)
        return {
            'refresh':str(tokens),
            'access':str(tokens.access_token)
        }"""
    
