from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="QR Code API",
        default_version="v1",
        description="A simple QR Code generator API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="bk22106@piusdev.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[path("qr/", include("qr.urls"))],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("qr.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    # Debug Toolbar 추가
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

    # DRF-YASG(Swagger, ReDoc) 추가
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
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
