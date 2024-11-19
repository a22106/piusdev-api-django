# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.LogOutView.as_view(), name="logout"),
    path("delete/", views.DeleteUserView.as_view(), name="delete_user"),
    path("verify-email/<str:uid>/<str:token>/", views.VerifyEmailView.as_view(), name="verify_email"),
]
