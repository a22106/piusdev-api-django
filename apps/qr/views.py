# qr/views.py
import traceback
from typing import Callable, List
from django.http import HttpResponse, JsonResponse
from PIL import Image
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import logging
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response

from apps.qr.constants import QRStyles, QRColorMasks, QREyeStyles

from apps.qr.constants.error_codes import QRErrorCodes, QRErrorMessages
from apps.qr.decorators import qr_swagger_decorator
from apps.qr.utils.qr_utils import (
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
    list_of_properties_of_serializer,
)
from apps.qr.serializers import *

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class BaseQrView(CreateAPIView):
    # GenericAPIView의 기능을 활용하기 위한 속성 설정
    serializer_class = None  # 각 하위 클래스에서 정의
    required_params = []

    def process_embedded_image(self, request: Request):
        embedded_image = None
        if 'embedded_image' in request.FILES:
            try:
                image_file = request.FILES['embedded_image']
                embedded_image = Image.open(image_file)
            except Exception as e:
                raise Response(
                    {
                        'detail': "Invalid embedded image file.",
                        'error_code': QRErrorCodes.INVALID_PARAMETERS
                    },
                    status=400
                )
        return embedded_image

    def post(self, request: Request, *args, **kwargs):
        """QR 코드 생성을 위한 POST 메서드"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'detail': serializer.errors,
                    'error_code': QRErrorCodes.INVALID_PARAMETERS
                },
                status=400
            )
        
        return self.handle_qr_generation(
            request,
            self.generator_func,
            self.required_params
        )

    def handle_qr_generation(self, request: Request, generator_func: Callable, required_params: List[str]):
        """QR 코드 생성 템플릿 메서드"""
        try:
            # 요청 데이터 로깅
            logger.debug(f"Request data: {request.data}")
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        'detail': serializer.errors,
                        'error_code': QRErrorCodes.INVALID_PARAMETERS
                    },
                    status=400
                )

            # 임베드 이미지 검증
            try:
                embedded_image = self.process_embedded_image(request)
            except ValueError as e:
                return Response(
                    {
                        'detail': str(e),
                        'error_code': QRErrorCodes.INVALID_IMAGE
                    },
                    status=400
                )

            # 요청 파라미터 준비
            generator_params = request.data
            generator_params['embedded_image'] = embedded_image

            # 파라미터 로깅
            logger.debug(f"Generator parameters: {generator_params}")

            # QR 코드 생성
            qr_image = generator_func(**generator_params)

            if not qr_image:
                return Response(
                    {
                        'detail': QRErrorMessages.get_message(QRErrorCodes.GENERATION_FAILED),
                        'error_code': QRErrorCodes.GENERATION_FAILED
                    },
                    status=500
                )

            # 응답 생성
            response = HttpResponse(qr_image, content_type="image/png")
            response['Content-Length'] = len(qr_image)
            response['Content-Disposition'] = 'inline; filename="qr-code.png"'

            # 성공 로깅
            logger.info(f"Successfully generated QR code: {len(qr_image)} bytes")

            return response

        except Exception as e:
            logger.error(f"Unexpected error generating QR Code: {str(e)}")
            traceback.print_exc()
            return Response(
                {
                    'detail': QRErrorMessages.get_message(QRErrorCodes.INTERNAL_ERROR),
                    'error_code': QRErrorCodes.INTERNAL_ERROR
                },
                status=500
            )



class QrUrlView(BaseQrView):
    serializer_class = UrlQRSerializer
    required_params = list_of_properties_of_serializer(UrlQRSerializer)
    
    @qr_swagger_decorator(
        "URL QR Code",
        UrlQRSerializer
    )
    def post(self, request: Request):
        return self.handle_qr_generation(request, generate_url_qr, self.required_params)

class QrVcardView(BaseQrView): # TODO: URL 제외 모든 QR코드 생성에 대한 테스트 코드 작성
    serializer_class = VCardQRSerializer
    required_params = list_of_properties_of_serializer(VCardQRSerializer)
    
    @qr_swagger_decorator(
        "VCard QR Code",
        VCardQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_vcard_qr, self.required_params)

class QrEmailView(BaseQrView):
    serializer_class = EmailQRSerializer
    required_params = list_of_properties_of_serializer(EmailQRSerializer)
    
    @qr_swagger_decorator(
        "Email QR Code",
        EmailQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_email_qr, self.required_params)


class QrTextView(BaseQrView):
    serializer_class = TextQRSerializer
    required_params = list_of_properties_of_serializer(TextQRSerializer)
    
    @qr_swagger_decorator(
        "Text QR Code",
        TextQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_text_qr, self.required_params)


class QrPhoneNumberView(BaseQrView):
    serializer_class = PhoneQRSerializer
    required_params = list_of_properties_of_serializer(PhoneQRSerializer)
    
    @qr_swagger_decorator(
        "Phone Number QR Code",
        PhoneQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_phone_qr, self.required_params)


class QrWifiView(BaseQrView):
    serializer_class = WiFiQRSerializer
    required_params = list_of_properties_of_serializer(WiFiQRSerializer)
    
    @qr_swagger_decorator(
        "WiFi QR Code",
        WiFiQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_wifi_qr, self.required_params)


class QrSmsView(BaseQrView):
    serializer_class = SMSQRSerializer
    required_params = list_of_properties_of_serializer(SMSQRSerializer)
    
    @qr_swagger_decorator(
        "SMS QR Code",
        SMSQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_sms_qr, self.required_params)


class QrGeoView(BaseQrView):
    serializer_class = GeoQRSerializer
    required_params = list_of_properties_of_serializer(GeoQRSerializer)
    
    @qr_swagger_decorator(
        "Geolocation QR Code",
        GeoQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_geo_qr, self.required_params)


class QrEventView(BaseQrView):
    serializer_class = EventQRSerializer
    required_params = list_of_properties_of_serializer(EventQRSerializer)
    
    @qr_swagger_decorator(
        "Event QR Code",
        EventQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_event_qr, self.required_params)


class QrMeCardView(BaseQrView):
    serializer_class = MeCardQRSerializer
    required_params = list_of_properties_of_serializer(MeCardQRSerializer)
    
    @qr_swagger_decorator(
        "MECARD QR Code",
        MeCardQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_mecard_qr, self.required_params)


class QrWhatsAppView(BaseQrView):
    serializer_class = WhatsAppQRSerializer
    required_params = list_of_properties_of_serializer(WhatsAppQRSerializer)
    
    @qr_swagger_decorator(
        "WhatsApp QR Code",
        WhatsAppQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_whatsapp_qr, self.required_params)


class QrBitcoinView(BaseQrView):
    serializer_class = BitcoinQRSerializer
    required_params = list_of_properties_of_serializer(BitcoinQRSerializer)
    
    @qr_swagger_decorator(
        "Bitcoin Payment QR Code",
        BitcoinQRSerializer
    )
    def post(self, request):
        return self.handle_qr_generation(request, generate_bitcoin_qr, self.required_params)
