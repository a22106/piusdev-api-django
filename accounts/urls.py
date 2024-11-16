# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Form 기반 뷰 (웹 페이지)
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('verify-email/<str:token>/', views.VerifyEmailView.as_view(), name='verify_email'),
    # API 엔드포인트
    path("api/logout/", views.SignOutView.as_view(), name="api_logout"),
    path("api/provider/", views.ProviderLoginView.as_view(), name="api_provider_login"),
    path("api/delete/", views.DeleteUserView.as_view(), name="api_delete_user"),
]
