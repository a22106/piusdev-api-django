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

    # POST 메서드를 제거하여 폼 제출이 AJAX로만 처리되도록 함
    # def post(self, request, *args, **kwargs):
    #     pass


class QrImageView(View):
    @method_decorator(require_http_methods(["POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        qr_type = request.POST.get("qr_type", "text")
        logger.info(f"Generating QR Code of type: {qr_type}")

        try:
            if qr_type == "url":
                url = request.POST.get("url", "")
                qr_image = generate_url_qr(url)
                display_text = url
            elif qr_type == "email":
                email = request.POST.get("email", "")
                subject = request.POST.get("subject", "")
                body = request.POST.get("body", "")
                qr_image = generate_email_qr(email, subject, body)
                display_text = email
            elif qr_type == "text":
                text = request.POST.get("text", "")
                qr_image = generate_text_qr(text)
                display_text = text
            elif qr_type == "phone":
                phone = request.POST.get("phone", "")
                qr_image = generate_phone_qr(phone)
                display_text = phone
            elif qr_type == "vcard":
                vcard_data = {
                    "first_name": request.POST.get("first_name", ""),
                    "last_name": request.POST.get("last_name", ""),
                    "vcard_email": request.POST.get("vcard_email", ""),
                    "vcard_mobile": request.POST.get("vcard_mobile", ""),
                    "organization": request.POST.get("organization", ""),
                    "title": request.POST.get("title", ""),
                    "address": request.POST.get("address", ""),
                    "label": request.POST.get("label", ""),
                    "vcard_url": request.POST.get("vcard_url", ""),
                    "note": request.POST.get("note", ""),
                }
                qr_image = generate_vcard_qr(vcard_data)
                display_text = f"{vcard_data.get('first_name', '')} {vcard_data.get('last_name', '')}"
            elif qr_type == "wifi":
                ssid = request.POST.get("ssid", "")
                password = request.POST.get("password", "")
                encryption = request.POST.get("encryption", "WPA")
                qr_image = generate_wifi_qr(ssid, password, encryption)
                display_text = ssid
            else:
                return HttpResponse("Invalid QR type.", status=400)

            return HttpResponse(qr_image, content_type="image/png")

        except Exception as e:
            logger.error(f"Error generating QR Code: {e}")
            return HttpResponse("Error generating QR Code.", status=500)


class QrUrlView(APIView):
    @swagger_auto_schema(
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
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Email address to encode in the QR Code",
                type=openapi.TYPE_STRING,
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
        manual_parameters=[
            openapi.Parameter(
                "text",
                openapi.IN_QUERY,
                description="Text to encode in the QR Code",
                type=openapi.TYPE_STRING,
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


class QrVCardView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "first_name",
                openapi.IN_QUERY,
                description="First name to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "last_name",
                openapi.IN_QUERY,
                description="Last name to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "vcard_email",
                openapi.IN_QUERY,
                description="Email to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "vcard_mobile",
                openapi.IN_QUERY,
                description="Mobile phone to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "organization",
                openapi.IN_QUERY,
                description="Organization to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "title",
                openapi.IN_QUERY,
                description="Title to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "address",
                openapi.IN_QUERY,
                description="Address to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "label",
                openapi.IN_QUERY,
                description="Label to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "vcard_url",
                openapi.IN_QUERY,
                description="URL to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "note",
                openapi.IN_QUERY,
                description="Note to encode in the QR Code",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate VCard QR Code")

        try:
            vcard_data = {
                "first_name": request.query_params.get("first_name", ""),
                "last_name": request.query_params.get("last_name", ""),
                "vcard_email": request.query_params.get("vcard_email", ""),
                "vcard_mobile": request.query_params.get("vcard_mobile", ""),
                "organization": request.query_params.get("organization", ""),
                "title": request.query_params.get("title", ""),
                "address": request.query_params.get("address", ""),
                "label": request.query_params.get("label", ""),
                "vcard_url": request.query_params.get("vcard_url", ""),
                "note": request.query_params.get("note", ""),
            }

            qr_image = generate_vcard_qr(vcard_data)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating VCard QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating VCard QR Code."}, status=500
            )


class QrWifiView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "ssid",  # Network name
                openapi.IN_QUERY,
                description="SSID to encode in the QR Code",
                type=openapi.TYPE_STRING,
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


class QrApiView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["qr_type"],
            properties={
                "qr_type": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Type of QR Code"
                ),
                "url": openapi.Schema(
                    type=openapi.TYPE_STRING, description="URL for URL QR Code"
                ),
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Email for Email QR Code"
                ),
                "subject": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Subject for Email QR Code"
                ),
                "body": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Body for Email QR Code"
                ),
                "text": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Text for Text QR Code"
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Phone number for Phone QR Code",
                ),
                "first_name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="First name for VCard QR Code"
                ),
                "last_name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Last name for VCard QR Code"
                ),
                "vcard_email": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Email for VCard QR Code"
                ),
                "vcard_mobile": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Mobile phone for VCard QR Code",
                ),
                "organization": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Organization for VCard QR Code",
                ),
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Title for VCard QR Code"
                ),
                "address": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Address for VCard QR Code"
                ),
                "label": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Label for VCard QR Code"
                ),
                "vcard_url": openapi.Schema(
                    type=openapi.TYPE_STRING, description="URL for VCard QR Code"
                ),
                "note": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Note for VCard QR Code"
                ),
                "ssid": openapi.Schema(
                    type=openapi.TYPE_STRING, description="SSID for WiFi QR Code"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Password for WiFi QR Code"
                ),
                "encryption": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Encryption type for WiFi QR Code",
                ),
            },
        ),
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def post(self, request):
        qr_type = request.data.get("qr_type", "text")
        logger.info(f"API Request to generate QR Code of type: {qr_type}")

        try:
            if qr_type == "url":
                url = request.data.get("url", "")
                qr_image = generate_url_qr(url)
                display_text = url
            elif qr_type == "email":
                email = request.data.get("email", "")
                subject = request.data.get("subject", "")
                body = request.data.get("body", "")
                qr_image = generate_email_qr(email, subject, body)
                display_text = email
            elif qr_type == "text":
                text = request.data.get("text", "")
                qr_image = generate_text_qr(text)
                display_text = text
            elif qr_type == "phone":
                phone = request.data.get("phone", "")
                qr_image = generate_phone_qr(phone)
                display_text = phone
            elif qr_type == "vcard":
                vcard_data = {
                    "first_name": request.data.get("first_name", ""),
                    "last_name": request.data.get("last_name", ""),
                    "vcard_email": request.data.get("vcard_email", ""),
                    "vcard_mobile": request.data.get("vcard_mobile", ""),
                    "organization": request.data.get("organization", ""),
                    "title": request.data.get("title", ""),
                    "address": request.data.get("address", ""),
                    "label": request.data.get("label", ""),
                    "vcard_url": request.data.get("vcard_url", ""),
                    "note": request.data.get("note", ""),
                }
                qr_image = generate_vcard_qr(vcard_data)
                display_text = f"{vcard_data.get('first_name', '')} {vcard_data.get('last_name', '')}"
            elif qr_type == "wifi":
                ssid = request.data.get("ssid", "")
                password = request.data.get("password", "")
                encryption = request.data.get("encryption", "WPA")
                qr_image = generate_wifi_qr(ssid, password, encryption)
                display_text = ssid
            else:
                return JsonResponse({"detail": "Invalid QR type."}, status=400)

            return HttpResponse(qr_image, content_type="image/png")

        except Exception as e:
            logger.error(f"Error generating QR Code via API: {e}")
            return JsonResponse({"detail": "Error generating QR Code."}, status=500)


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
