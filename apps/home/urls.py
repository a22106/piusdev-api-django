from django.urls import path
from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "home"

schema_view = get_schema_view(
    openapi.Info(
        title="QR Code Generator API",
        default_version="v1",
        description="A simple QR Code generator API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="bk22106@piusdev.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("api/", schema_view.with_ui("redoc", cache_timeout=0), name="api"),
    path("", views.IndexView.as_view(), name="index"),
]