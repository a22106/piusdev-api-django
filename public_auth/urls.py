from django.urls import path
from . import views

app_name = "public_auth"

urlpatterns = [
    path("v1/signup/", views.SignupView.as_view(), name="signup"),
    path("v1/login/", views.LoginView.as_view(), name="login"),
]
