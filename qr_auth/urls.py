from django.urls import path
from . import views

app_name = "qr_auth"

urlpatterns = [
    path("", views.LoginPageView.as_view(), name="login_page"),
    path("v1/signup/", views.SignupView.as_view(), name="signup"),
    path("v1/login/", views.LoginView.as_view(), name="login"),
    path("v1/logout/", views.LogoutView.as_view(), name="logout"),
]
