from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('phonenumber-verify/', VerifyPhonenumber.as_view(), name="phonenumber-verify"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
