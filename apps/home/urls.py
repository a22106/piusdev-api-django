from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    # 홈페이지 메인 뷰
    path("", views.HomeView.as_view(), name="index"),
]