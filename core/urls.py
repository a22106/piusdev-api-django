from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


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
    patterns=[
        path("", include("qr.urls")),
    ],
)

urlpatterns = [
    path("pius_hwang/", admin.site.urls),
    path("", include("qr.urls", namespace="qr")),
    # API Documentation
    path("api/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("auth/", include("public_auth.urls", namespace="auth")),
]

if settings.DEBUG:
    import debug_toolbar

    # Debug Toolbar addition
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

    # DRF-YASG (Swagger, ReDoc) addition
    urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]
