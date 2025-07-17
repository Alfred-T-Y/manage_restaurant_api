from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('phonenumber-verify/', VerifPhonenumber.as_view(), name="phonenumber-verify")
]
