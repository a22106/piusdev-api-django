# qr/views.py
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging

from rest_framework.views import APIView

from qr.utils.qr_utils import (
    generate_url_qr,
    generate_email_qr,
    generate_text_qr,
    generate_phone_qr,
    generate_vcard_qr,
    generate_wifi_qr,
)

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "qr/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "QR Code Generator"
        context["description"] = "A simple QR Code generator"
        context["keywords"] = "QR Code, Generator"
        return context


# TODO: vcard Email 입력이 안되는 문제 있음
class QrVcardView(APIView):
    @swagger_auto_schema(
        operation_id="VCard QR Code",
        manual_parameters=[
            openapi.Parameter(
                "first_name",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "last_name",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "phone",
                openapi.IN_QUERY,
                description="Phone number",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "mobile",
                openapi.IN_QUERY,
                description="Mobile phone number",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Email address",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "website",
                openapi.IN_QUERY,
                description="Website URL",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "organization",
                openapi.IN_QUERY,
                description="Organization",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "job_title",
                openapi.IN_QUERY,
                description="Job title",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "fax",
                openapi.IN_QUERY,
                description="Fax number",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "address",
                openapi.IN_QUERY,
                description="Address",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "zip",
                openapi.IN_QUERY,
                description="Zip code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "country",
                openapi.IN_QUERY,
                description="Country",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "note",
                openapi.IN_QUERY,
                description="Note",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        try:
            qr_image = generate_vcard_qr(request.query_params)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating VCard QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating VCard QR Code."}, status=500
            )


class QrUrlView(APIView):
    @swagger_auto_schema(
        operation_id="URL QR Code",
        manual_parameters=[
            openapi.Parameter(
                "url",
                openapi.IN_QUERY,
                description="URL to encode in the QR Code",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate URL QR Code")

        try:
            url = request.query_params.get("url", "")
            if not url:
                return JsonResponse(
                    {"detail": "URL parameter is required."}, status=400
                )
            qr_image = generate_url_qr(url)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating URL QR Code via API: {e}")
            return JsonResponse({"detail": "Error generating URL QR Code."}, status=500)


class QrEmailView(APIView):
    @swagger_auto_schema(
        operation_id="Email QR Code",
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Email address to encode in the QR Code",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "subject",
                openapi.IN_QUERY,
                description="Subject to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "body",
                openapi.IN_QUERY,
                description="Body to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate Email QR Code")

        try:
            email = request.query_params.get("email", "")
            subject = request.query_params.get("subject", "")
            body = request.query_params.get("body", "")
            if not email:
                return JsonResponse(
                    {"detail": "Email parameter is required."}, status=400
                )

            qr_image = generate_email_qr(email, subject, body)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating Email QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating Email QR Code."}, status=500
            )


class QrTextView(APIView):
    @swagger_auto_schema(
        operation_id="Text QR Code",
        manual_parameters=[
            openapi.Parameter(
                "text",
                openapi.IN_QUERY,
                description="Text to encode in the QR Code",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate Text QR Code")

        try:
            text = request.query_params.get("text", "")
            if not text:
                return JsonResponse(
                    {"detail": "Text parameter is required."}, status=400
                )

            qr_image = generate_text_qr(text)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating Text QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating Text QR Code."}, status=500
            )


class QrPhoneNumberView(APIView):
    @swagger_auto_schema(
        operation_id="Phone Number QR Code",
        manual_parameters=[
            openapi.Parameter(
                "phone",
                openapi.IN_QUERY,
                description="Phone number to encode in the QR Code",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate Phone QR Code")

        try:
            phone = request.query_params.get("phone", "")
            if not phone:
                return JsonResponse(
                    {"detail": "Phone parameter is required."}, status=400
                )

            qr_image = generate_phone_qr(phone)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating Phone QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating Phone QR Code."}, status=500
            )


class QrWifiView(APIView):
    @swagger_auto_schema(
        operation_id="WiFi QR Code",
        manual_parameters=[
            openapi.Parameter(
                "ssid",  # Network name
                openapi.IN_QUERY,
                description="SSID to encode in the QR Code",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "password",
                openapi.IN_QUERY,
                description="Password to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "encryption",  # Network security type(WEP, WPA/WPA2, None)
                openapi.IN_QUERY,
                description="Encryption type to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate WiFi QR Code")

        try:
            ssid = request.query_params.get("ssid", "")
            password = request.query_params.get("password", "")
            encryption = request.query_params.get("encryption", "WPA")
            if not ssid:
                return JsonResponse(
                    {"detail": "SSID parameter is required."}, status=400
                )

            qr_image = generate_wifi_qr(ssid, password, encryption)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating WiFi QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating WiFi QR Code."}, status=500
            )


# Swagger endpoint response {"detail": "Hello World"}
class HelloWorldView(APIView):
    @swagger_auto_schema(
        operation_description="This is a test view",
        responses={200: openapi.Response("Hello World")},
    )
    def get(self, request):
        return HttpResponse("Hello World")


class HelloDjangoView(APIView):
    @swagger_auto_schema(
        operation_description="This is a test view",
        responses={200: openapi.Response("Hello Django")},
    )
    def post(self, request):
        return HttpResponse("Hello Django")
