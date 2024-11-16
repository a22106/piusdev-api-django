from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Form 기반 뷰 (웹 페이지)
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    # API 엔드포인트
    path("api/logout/", views.LogoutView.as_view(), name="api_logout"),
    path("api/provider/", views.ProviderLoginView.as_view(), name="api_provider_login"),
    path("api/delete/", views.DeleteUserView.as_view(), name="api_delete_user"),
]
