from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager,PermissionsMixin)
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumber_field.modelfields import PhoneNumberField
#from rest_framework_simplejwt.tokens import RefreshToken





class UserManager(BaseUserManager):
    def normalize_phone(self, phone):
        try:
            phone=str(phone)
            # On suppose que le numéro est au format international ou commence par +
            parsed = phonenumbers.parse(phone, None)  # Pas de région forcée

            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Phone number invalid.")

            # Retourne au format E.164 : +1234567890
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    
        except NumberParseException as e:
            raise ValueError("The phone number is in a invalid format") from e

    def create_user(self, email, username, phonenumber, role=None,password=None):
        
        if email is None:
            raise TypeError('The Email is required')
        if username is None:
            raise TypeError('The Name is required')
        if phonenumber is None:
            raise TypeError('The phone number is required')

        user = self.model(
            email=self.normalize_email(email),
            phonenumber=self.normalize_phone(phonenumber),
            username=username,
        )
        role=role
        user.set_password("sal"+password+"age")
        user.save()
        return user

    def create_superuser(self, email, username, phonenumber, role=None ,password=None):

        if password is None:
            raise TypeError('The Password is required')

        user = self.create_user(email, username, phonenumber,role, password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):

    ROLE = [
        ('OWNER','Owner'),
        ('MANAGER','Manager'),
        ('DELIVER','Deliver'),
        ('KITCHENMANAGER','Kitchen_manager'),
        ('WAITER','Waiter')
    ]
    role = models.CharField(choices=ROLE, max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phonenumber = PhoneNumberField(unique=True, db_index=True, region=None)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email_is_verified = models.BooleanField(default=False)
    phonenumber_is_verified = models.BooleanField(default=False)
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
    
#admin model
class Owner(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner')
    
    def delete(self, *args, **kwargs):
        for manager in self.managers.all():
            manager.user.delete()
        for waiter in self.waiters.all():
            waiter.user.delete()
        for kitchen_manager in self.kitchen_managers.all():
            kitchen_manager.user.delete()
        for deliver in self.delivers.all():
            deliver.user.delete()
        # Supprimer l'utilisateur lié
        self.user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.user.username
    

#manager model
class Manager(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='managers')
    
    def __str__(self):
        return self.user.username


#waiter model
class Waiter(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='waiter')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='waiters')

    def __str__(self):
        return self.user.username


#kitchen_manager model
class KitchenManager(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kitchen_manager')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='kitchen_managers')

    def __str__(self):
        return self.user.username
    

#deliver model
class Deliver(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='deliver')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='delivers')

    def __str__(self):
        return self.user.username