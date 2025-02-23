from PIL import ImageColor

from rest_framework import serializers

from apps.qr.constants.enums import *

class BaseQRSerializer(serializers.Serializer):
    """기본 QR 코드 생성 공통 필드"""
    style = serializers.ChoiceField(
        choices=QRStyles.get_all_styles(),
        default=QRStyles.SQUARE_MODULE.value
    )
    fill_color = serializers.CharField(default='black')
    back_color = serializers.CharField(default='white')
    color_mask = serializers.ChoiceField(
        choices=QRColorMasks.get_all_color_masks(),
        default=QRColorMasks.SOLID_FILL.value
    )
    embedded_image = serializers.ImageField(required=False)
    embedded_image_ratio = serializers.FloatField(
        default=0.25,
        min_value=0.1,
        max_value=0.5
    )
    
    def _color_validator(self, value):
        """색상 형식 검증"""
        try:
            ImageColor.getrgb(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
    def validate_fill_color(self, value):
        """fill_color 검증"""
        self._color_validator(value)
        return value
    
    def validate_back_color(self, value):
        """back_color 검증"""
        self._color_validator(value)
        return value


class UrlQRSerializer(BaseQRSerializer):
    """URL QR 코드 생성 Serializer"""
    url = serializers.CharField()

    def validate_url(self, value):
        """URL 형식 검증
        - http://, https:// 로 시작하는 URL 허용
        - example.com 같은 도메인 형식도 허용
        """
        # 프로토콜이 없는 경우 'https://'를 기본값으로 추가
        if not value.startswith(('http://', 'https://')):
            value = f'https://{value}'
            
        # 최소한의 도메인 형식 검증 (예: xxx.xxx)
        parts = value.split('://')[-1].split('.')
        if len(parts) < 2 or not all(parts):
            raise serializers.ValidationError("Invalid URL format. Please provide a valid domain (e.g., example.com)")
            
        return value

class QrResponseSerializer(serializers.Serializer):
    """URL QR 코드 생성 응답 Serializer"""
    qr_code = serializers.ImageField()

class QrErrorResponseSerializer(serializers.Serializer):
    """QR 코드 생성 실패 응답 Serializer"""
    detail = serializers.CharField()
    error_code = serializers.CharField(required=False)

class EmailQRSerializer(BaseQRSerializer):
    """이메일 QR 코드 생성 Serializer"""
    email = serializers.EmailField()
    subject = serializers.CharField(required=False, allow_blank=True)
    body = serializers.CharField(required=False, allow_blank=True)

class TextQRSerializer(BaseQRSerializer):
    """텍스트 QR 코드 생성 Serializer"""
    text = serializers.CharField()

class PhoneQRSerializer(BaseQRSerializer):
    """전화번호 QR 코드 생성 Serializer"""
    country_code = serializers.CharField(required=False, allow_blank=True, default='+1')
    phone_number = serializers.CharField()

class VCardQRSerializer(BaseQRSerializer):
    """VCard QR 코드 생성 Serializer"""
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    vcard_mobile = serializers.CharField()
    vcard_email = serializers.EmailField()
    vcard_url = serializers.URLField(required=False, allow_blank=True)
    organization = serializers.CharField(required=False, allow_blank=True)
    job_title = serializers.CharField(required=False, allow_blank=True)
    fax = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    zip = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    note = serializers.CharField(required=False, allow_blank=True)

class WiFiQRSerializer(BaseQRSerializer):
    """WiFi QR 코드 생성 Serializer"""
    ssid = serializers.CharField()
    password = serializers.CharField(required=False, allow_blank=True)
    encryption = serializers.ChoiceField(
        choices=[(enc.value, enc.name) for enc in WifiEncryption],
        default=WifiEncryption.WPA.value
    )
    hidden = serializers.BooleanField(default=False)

class SMSQRSerializer(BaseQRSerializer):
    """SMS QR 코드 생성 Serializer"""
    phone_number = serializers.CharField()
    message = serializers.CharField(required=False, allow_blank=True)

class GeoQRSerializer(BaseQRSerializer):
    """위치 QR 코드 생성 Serializer"""
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    query = serializers.CharField(required=False, allow_blank=True)
    zoom = serializers.IntegerField(default=0, min_value=0, max_value=20)

class EventQRSerializer(BaseQRSerializer):
    """이벤트 QR 코드 생성 Serializer"""
    title = serializers.CharField()
    start = serializers.CharField()  # YYYYMMDD 형식
    end = serializers.CharField()    # YYYYMMDD 형식
    location = serializers.CharField()
    description = serializers.CharField()

    def validate_start(self, value):
        """시작 날짜 형식 검증"""
        if len(value) != 8 or not value.isdigit():
            raise serializers.ValidationError("Start date must be in YYYYMMDD format.")
        return value

    def validate_end(self, value):
        """종료 날짜 형식 검증"""
        if len(value) != 8 or not value.isdigit():
            raise serializers.ValidationError("End date must be in YYYYMMDD format.")
        return value

class MeCardQRSerializer(BaseQRSerializer):
    """MeCard QR 코드 생성 Serializer"""
    name = serializers.CharField()
    reading = serializers.CharField()
    tel = serializers.CharField()
    email = serializers.EmailField()
    memo = serializers.CharField(required=False, allow_blank=True)
    birthday = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    url = serializers.URLField(required=False, allow_blank=True)
    nickname = serializers.CharField(required=False, allow_blank=True)

class WhatsAppQRSerializer(BaseQRSerializer):
    """WhatsApp QR 코드 생성 Serializer"""
    phone_number = serializers.CharField()
    message = serializers.CharField(required=False, allow_blank=True)

class BitcoinQRSerializer(BaseQRSerializer):
    """비트코인 QR 코드 생성 Serializer"""
    address = serializers.CharField()
    amount = serializers.FloatField(required=False)
    label = serializers.CharField(required=False, allow_blank=True)
    message = serializers.CharField(required=False, allow_blank=True)