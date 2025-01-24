from core import settings
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="QR Code Generator API",
        default_version="v0.0.1",
        description="A simple QR Code generator API",
        contact=openapi.Contact(email="piushwang@piusdev.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include("apps.home.urls", namespace="home")),
    path("pius_hwang/", admin.site.urls),
    
    # API v1 엔드포인트
    path('api/v1/', include([
        path('qr/', include('apps.qr.urls')),
        path('auth/', include('apps.accounts.urls', namespace='accounts')),
    ])),
    
    # API Documentation
    path("api/docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    
    # 통합 테스트
    path("", include("django_cypress.urls")),
]

if settings.DEBUG:
    # Debug Toolbar addition
    urlpatterns += [path("__debug__/", include('debug_toolbar.urls'))]

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
