# accounts/urls.py
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "accounts"

urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.LogOutView.as_view(), name="logout"),
    path("delete/", views.DeleteUserView.as_view(), name="delete_user"),

    path("verify-email/<str:uid>/<str:token>/", views.VerifyEmailView.as_view(), name="verify_email"),
]
