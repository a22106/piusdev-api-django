# qr/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
import pycountry
import phonenumbers

from rest_framework.views import APIView

from qr.utils.qr_utils import (
    generate_url_qr,
    generate_email_qr,
    generate_text_qr,
    generate_phone_qr,
    generate_vcard_qr,
    generate_wifi_qr,
    generate_sms_qr,
    generate_bitcoin_qr,
    generate_whatsapp_qr,
    generate_mecard_qr,
    generate_event_qr,
    generate_geo_qr,
)

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    def get(self, request):
        countries = []
        for country in sorted(pycountry.countries, key=lambda x: x.name):
            try:
                country_code = phonenumbers.country_code_for_region(country.alpha_2)
                countries.append(
                    {
                        "name": country.name,
                        "dial_code": f"+{country_code}",
                    }
                )
            except:
                continue  # 국가 코드가 없는 경우 건너뜀

        context = {
            "countries": countries,
            # 추가 context
        }
        return render(request, "qr/index.html", context)

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
                "vcard_phone",
                openapi.IN_QUERY,
                description="Phone number",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "vcard_mobile",
                openapi.IN_QUERY,
                description="Mobile phone number",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "vcard_email",
                openapi.IN_QUERY,
                description="Email address",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "vcard_url",
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
                "phone_number",
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
            phone_number = request.query_params.get("phone_number", "")
            if not phone_number:
                return JsonResponse(
                    {"detail": "Phone parameter is required."}, status=400
                )

            qr_image = generate_phone_qr(phone_number)
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


class QrSmsView(APIView):
    @swagger_auto_schema(
        operation_id="SMS QR Code",
        manual_parameters=[
            openapi.Parameter(
                "country_code",
                openapi.IN_QUERY,
                description="Country code",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "phone_number",
                openapi.IN_QUERY,
                description="Phone number",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "message",
                openapi.IN_QUERY,
                description="SMS message",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate SMS QR Code")
        try:
            phone_number = request.query_params.get("phone_number", "")
            message = request.query_params.get("message", "")

            if not phone_number or not message:
                return JsonResponse(
                    {
                        "detail": "Country code, phone number, and message parameters are required."
                    },
                    status=400,
                )

            qr_image = generate_sms_qr(phone_number, message)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating SMS QR Code via API: {e}")
            return JsonResponse({"detail": "Error generating SMS QR Code."}, status=500)


class QrGeoView(APIView):
    @swagger_auto_schema(
        operation_id="Geographical Location QR Code",
        manual_parameters=[
            openapi.Parameter(
                "latitude",
                openapi.IN_QUERY,
                description="Latitude of the location",
                type=openapi.TYPE_NUMBER,
                required=True,
            ),
            openapi.Parameter(
                "longitude",
                openapi.IN_QUERY,
                description="Longitude of the location",
                type=openapi.TYPE_NUMBER,
                required=True,
            ),
            openapi.Parameter(
                "query",
                openapi.IN_QUERY,
                description="Optional query parameter (e.g., place name)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "zoom",
                openapi.IN_QUERY,
                description="Optional zoom level",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate Geo QR Code")
        try:
            latitude = request.query_params.get("latitude", None)
            longitude = request.query_params.get("longitude", None)
            query = request.query_params.get("query", "")
            zoom = request.query_params.get("zoom", 0)

            if latitude is None or longitude is None:
                return JsonResponse(
                    {"detail": "Latitude and longitude parameters are required."},
                    status=400,
                )

            # Convert latitude and longitude to floats
            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                return JsonResponse(
                    {"detail": "Latitude and longitude must be valid numbers."},
                    status=400,
                )

            # Convert zoom to int
            try:
                zoom = int(zoom)
            except ValueError:
                zoom = 0  # default value

            qr_image = generate_geo_qr(latitude, longitude, query, zoom)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating Geo QR Code via API: {e}")
            return JsonResponse({"detail": "Error generating Geo QR Code."}, status=500)


class QrEventView(APIView):
    @swagger_auto_schema(
        operation_id="Calendar Event QR Code",
        manual_parameters=[
            openapi.Parameter(
                "summary",
                openapi.IN_QUERY,
                description="Event summary or title",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description="Event start date in YYYYMMDDTHHMMSSZ format",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description="Event end date in YYYYMMDDTHHMMSSZ format",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "location",
                openapi.IN_QUERY,
                description="Event location",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "description",
                openapi.IN_QUERY,
                description="Event description",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate Event QR Code")
        try:
            summary = request.query_params.get("summary", "")
            start_date = request.query_params.get("start_date", "")
            end_date = request.query_params.get("end_date", "")
            location = request.query_params.get("location", "")
            description = request.query_params.get("description", "")

            if not summary or not start_date or not end_date:
                return JsonResponse(
                    {
                        "detail": "summary, start_date, and end_date parameters are required."
                    },
                    status=400,
                )

            event_data = {
                "summary": summary,
                "start_date": start_date,
                "end_date": end_date,
                "location": location,
                "description": description,
            }

            qr_image = generate_event_qr(event_data)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating Event QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating Event QR Code."}, status=500
            )


class QrMeCardView(APIView):
    @swagger_auto_schema(
        operation_id="MECARD QR Code",
        manual_parameters=[
            openapi.Parameter(
                "name",
                openapi.IN_QUERY,
                description="Name of the contact",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "reading",
                openapi.IN_QUERY,
                description="Phonetic reading of the name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "tel",
                openapi.IN_QUERY,
                description="Telephone number",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Email address",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "memo",
                openapi.IN_QUERY,
                description="Memo or note",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "birthday",
                openapi.IN_QUERY,
                description="Birthday in YYYYMMDD format",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "address",
                openapi.IN_QUERY,
                description="Address",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "url",
                openapi.IN_QUERY,
                description="Website URL",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "nickname",
                openapi.IN_QUERY,
                description="Nickname",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate MECARD QR Code")
        try:
            name = request.query_params.get("name", "")
            if not name:
                return JsonResponse(
                    {"detail": "Name parameter is required."}, status=400
                )

            mecard_data = {
                "name": name,
                "reading": request.query_params.get("reading", ""),
                "tel": request.query_params.get("tel", ""),
                "email": request.query_params.get("email", ""),
                "memo": request.query_params.get("memo", ""),
                "birthday": request.query_params.get("birthday", ""),
                "address": request.query_params.get("address", ""),
                "url": request.query_params.get("url", ""),
                "nickname": request.query_params.get("nickname", ""),
            }

            qr_image = generate_mecard_qr(mecard_data)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating MECARD QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating MECARD QR Code."}, status=500
            )


class QrWhatsAppView(APIView):
    @swagger_auto_schema(
        operation_id="WhatsApp QR Code",
        manual_parameters=[
            openapi.Parameter(
                "phone_number",
                openapi.IN_QUERY,
                description="Recipient's phone number in international format",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "message",
                openapi.IN_QUERY,
                description="Message to send",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate WhatsApp QR Code")
        try:
            print(request.query_params)
            phone_number = request.query_params.get("phone_number", "")
            message = request.query_params.get("message", "")

            if not phone_number:
                return JsonResponse(
                    {"detail": "phone_number parameter is required."}, status=400
                )

            qr_image = generate_whatsapp_qr(phone_number, message)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating WhatsApp QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating WhatsApp QR Code."}, status=500
            )


class QrBitcoinView(APIView):
    @swagger_auto_schema(
        operation_id="Bitcoin Payment QR Code",
        manual_parameters=[
            openapi.Parameter(
                "address",
                openapi.IN_QUERY,
                description="Bitcoin wallet address",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "amount",
                openapi.IN_QUERY,
                description="Amount in BTC",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "label",
                openapi.IN_QUERY,
                description="Label for the payment",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "message",
                openapi.IN_QUERY,
                description="Message or note",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def get(self, request):
        logger.info("API Request to generate Bitcoin QR Code")
        try:
            address = request.query_params.get("address", "")
            amount = request.query_params.get("amount", None)
            label = request.query_params.get("label", "")
            message = request.query_params.get("message", "")

            if not address:
                return JsonResponse(
                    {"detail": "address parameter is required."}, status=400
                )

            # Convert amount to float if provided
            if amount:
                try:
                    amount = float(amount)
                except ValueError:
                    return JsonResponse(
                        {"detail": "amount must be a valid number."}, status=400
                    )
            else:
                amount = None

            qr_image = generate_bitcoin_qr(address, amount, label, message)
            return HttpResponse(qr_image, content_type="image/png")
        except Exception as e:
            logger.error(f"Error generating Bitcoin QR Code via API: {e}")
            return JsonResponse(
                {"detail": "Error generating Bitcoin QR Code."}, status=500
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
