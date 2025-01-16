import json
from django.test import TestCase, Client
from django.urls import reverse
from PIL import Image
from io import BytesIO

class QRCodeGenerationTest(TestCase):
    def setUp(self):
        """테스트를 위한 초기 설정"""
        self.client = Client()
        self.common_params = {
            "style": "SQUARE_MODULE",
            "fill_color": "black",
            "back_color": "white",
            "color_mask": "SOLID_FILL",
            "embedded_image_ratio": 0.2
        }

    def _validate_qr_response(self, response):
        """QR 코드 응답 검증을 위한 헬퍼 메서드"""
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        
        # 응답이 유효한 이미지인지 확인
        image = Image.open(BytesIO(response.content))
        self.assertEqual(image.format, 'PNG')

    def test_url_qr_generation(self):
        """URL QR 코드 생성 테스트"""
        url = reverse('qr:qr_url_v1')
        data = {
            "url": "https://www.example.com",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self._validate_qr_response(response)

    def test_email_qr_generation(self):
        """이메일 QR 코드 생성 테스트"""
        url = reverse('qr:qr_email_v1')
        data = {
            "email": "test@example.com",
            "subject": "Test Subject",
            "body": "Test Body",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self._validate_qr_response(response)

    def test_text_qr_generation(self):
        """텍스트 QR 코드 생성 테스트"""
        url = reverse('qr:qr_text_v1')
        data = {
            "text": "Hello, World!",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self._validate_qr_response(response)

    def test_phone_qr_generation(self):
        """전화번호 QR 코드 생성 테스트"""
        url = reverse('qr:qr_phone_number_v1')
        data = {
            "phone_number": "+821012345678",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self._validate_qr_response(response)

    def test_wifi_qr_generation(self):
        """WiFi QR 코드 생성 테스트"""
        url = reverse('qr:qr_wifi_v1')
        data = {
            "ssid": "TestWiFi",
            "password": "testpassword",
            "encryption": "WPA",
            "hidden": False,
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self._validate_qr_response(response)

    def test_vcard_qr_generation(self):
        """VCard QR 코드 생성 테스트"""
        url = reverse('qr:qr_vcard_v1')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "vcard_mobile": "+821012345678",
            "vcard_email": "john@example.com",
            "organization": "Test Corp",
            "job_title": "Developer",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self._validate_qr_response(response)

    def test_invalid_parameters(self):
        """잘못된 파라미터 테스트"""
        url = reverse('qr:qr_url_v1')
        data = {
            "style": "INVALID_STYLE",
            "url": "https://www.example.com"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_required_parameters(self):
        """필수 파라미터 누락 테스트"""
        url = reverse('qr:qr_url_v1')
        data = {
            **self.common_params
            # url 파라미터 누락
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

class QRCodeAdvancedGenerationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.common_params = {
            "style": "SQUARE_MODULE",
            "fill_color": "black", 
            "back_color": "white",
            "color_mask": "SOLID_FILL",
            "embedded_image_ratio": 0.2
        }

    def test_geo_qr_generation(self):
        """지리 정보 QR 코드 생성 테스트"""
        url = reverse('qr:qr_geo_v1')
        data = {
            "latitude": "37.5665",
            "longitude": "126.9780",
            "query": "Seoul City Hall",
            "zoom": "15",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_event_qr_generation(self):
        """이벤트 QR 코드 생성 테스트"""
        url = reverse('qr:qr_event_v1')
        data = {
            "title": "Test Event",
            "start": "20240101",
            "end": "20240102",
            "location": "Test Location",
            "description": "Test Description",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_mecard_qr_generation(self):
        """MECard QR 코드 생성 테스트"""
        url = reverse('qr:qr_mecard_v1')
        data = {
            "name": "John Doe",
            "reading": "jon do",
            "tel": "+821012345678",
            "email": "john@example.com",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_whatsapp_qr_generation(self):
        """WhatsApp QR 코드 생성 테스트"""
        url = reverse('qr:qr_whatsapp_v1')
        data = {
            "phone_number": "821012345678",
            "message": "Hello from test",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_bitcoin_qr_generation(self):
        """Bitcoin QR 코드 생성 테스트"""
        url = reverse('qr:qr_bitcoin_v1')
        data = {
            "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "amount": 0.001,
            "label": "Test Payment",
            "message": "Test Bitcoin Payment",
            **self.common_params
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_color_variations(self):
        """다양한 색상 조합 테스트"""
        url = reverse('qr:qr_text_v1')
        color_tests = [
            {"fill_color": "red", "back_color": "white"},
            {"fill_color": "#FF0000", "back_color": "#FFFFFF"},
            {"fill_color": "rgb(255,0,0)", "back_color": "rgb(255,255,255)"}
        ]
        
        for colors in color_tests:
            data = {
                "text": "Color Test",
                **self.common_params,
                **colors
            }
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 200)

    def test_style_variations(self):
        """다양한 스타일 테스트"""
        url = reverse('qr:qr_text_v1')
        styles = [
            "SQUARE_MODULE",
            "GAPPED_SQUARE_MODULE",
            "CIRCLE_MODULE",
            "ROUNDED_MODULE",
            "HORIZONTAL_BARS",
            "VERTICAL_BARS"
        ]
        
        for style in styles:
            data = {
                "text": "Style Test",
                **self.common_params,
                "style": style
            }
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 200) 