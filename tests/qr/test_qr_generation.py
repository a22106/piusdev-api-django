# tests/qr/test_qr_generation.py
from django.urls import reverse
from PIL import Image
from io import BytesIO
import pytest
from unittest.mock import patch, Mock

from apps.qr.constants.enums import QRColorMasks, QRStyles
from apps.qr.constants.error_codes import QRErrorCodes, QRErrorMessages

@pytest.fixture
def common_params():
    return {
        "style": QRStyles.SQUARE_MODULE.value,
        "fill_color": "black",
        "back_color": "white",
        "color_mask": QRColorMasks.SOLID_FILL.value,
        "embedded_image_ratio": 0.2
    }

@pytest.fixture
def mock_qr_url_request(common_params):
    request_body = {
        "url": "https://www.example.com",
        **common_params
    }
    return request_body

@pytest.mark.django_db
class QrTestBase:
    view_name = ''
    mock_qr_request = {}
    
    def _validate_qr_response(self, response):
        """QR 코드 응답 검증을 위한 헬퍼 메서드"""
        assert response.status_code == 200
        assert response.get('Content-Type') == 'image/png'
        
        # 응답이 유효한 이미지인지 확인
        image = Image.open(BytesIO(response.content))
        assert image.format == 'PNG'
        
    def test_qr_invalid_style(self, client):
        """잘못된 스타일 파라미터 테스트"""
        url = reverse(self.view_name)
        qr_request = self.mock_qr_request.copy()
        qr_request['style'] = 'INVALID_STYLE'
        response = client.post(url, data=qr_request)
        assert response.status_code == 400
        assert 'style' in response.json()['detail'].keys()
        assert response.json()['error_code'] == QRErrorCodes.INVALID_PARAMETERS

    def test_qr_invalid_color_mask(self, client):
        """잘못된 컬러 마스크 테스트"""
        url = reverse(self.view_name)
        qr_request = self.mock_qr_request.copy()
        qr_request['color_mask'] = 'INVALID_MASK'
        
        response = client.post(url, data=qr_request)
        
        assert response.status_code == 400
        assert 'color_mask' in response.json()['detail'].keys()
        assert response.json()['error_code'] == QRErrorCodes.INVALID_PARAMETERS

    def test_qr_invalid_image_ratio(self, client):
        """잘못된 이미지 비율 테스트"""
        url = reverse(self.view_name)
        qr_request = self.mock_qr_request.copy()
        qr_request['embedded_image_ratio'] = 0.6  # 허용 범위 초과
        
        response = client.post(url, data=qr_request)
        
        assert response.status_code == 400
        assert 'embedded_image_ratio' in response.json()['detail'].keys()
        assert response.json()['error_code'] == QRErrorCodes.INVALID_PARAMETERS

    def test_qr_invalid_color(self, client):
        """잘못된 색상 테스트"""
        url = reverse(self.view_name)
        qr_request = self.mock_qr_request.copy()
        qr_request['fill_color'] = 'invalid-color'
        
        response = client.post(url, data=qr_request)
        
        assert response.status_code == 400
        assert 'fill_color' in response.json()['detail'].keys()
        assert response.json()['error_code'] == QRErrorCodes.INVALID_PARAMETERS
        
    def test_qr_with_different_styles(self, client):
        """다양한 스타일 테스트"""
        url = reverse(self.view_name)
        styles = QRStyles.get_all_styles()
        
        for style in styles:
            self.mock_qr_request['style'] = style
            response = client.post(url, data=self.mock_qr_request)
            self._validate_qr_response(response)

    def test_qr_with_different_colors(self, client):
        """다양한 색상 조합 테스트"""
        url = reverse(self.view_name)
        color_tests = [
            {"fill_color": "red", "back_color": "white"},
            {"fill_color": "#FF0000", "back_color": "#FFFFFF"},
            {"fill_color": "rgb(255,0,0)", "back_color": "rgb(255,255,255)"}
        ]
        
        for colors in color_tests:
            self.mock_qr_request.update(colors)
            response = client.post(url, data=self.mock_qr_request)
            self._validate_qr_response(response)

    
    def test_qr_with_different_masks(self, client):
        """다양한 컬러 마스크 테스트"""
        url = reverse(self.view_name)
        masks = QRColorMasks.get_all_color_masks()
        
        for mask in masks:
            self.mock_qr_request['color_mask'] = mask
            response = client.post(url, data=self.mock_qr_request)
            self._validate_qr_response(response)
            
@pytest.mark.django_db
class TestQRUrlEndpoint(QrTestBase):
    view_name = 'qr:qr_url_v1'
    mock_qr_request = {
        "url": "https://www.example.com",
        "style": QRStyles.SQUARE_MODULE.value,
        "fill_color": "black",
        "back_color": "white",
        "color_mask": QRColorMasks.SOLID_FILL.value,
        "embedded_image_ratio": 0.2
    }
    
    def test_url_qr_generation_success(self, client):
        """기본 URL QR 코드 생성 테스트"""
        url = reverse(self.view_name)
        response = client.post(url, data=self.mock_qr_request)
        self._validate_qr_response(response)

    def test_url_qr_missing_parameters(self, client):
        """필수 파라미터 누락 테스트"""
        url = reverse(self.view_name)
        response = client.post(url, data={})
        
        assert response.status_code == 400
        assert 'url' in response.json()['detail'].keys()
        assert response.json()['error_code'] == QRErrorCodes.INVALID_PARAMETERS

    def test_url_qr_invalid_parameters(self, client):
        """잘못된 파라미터 테스트"""
        url = reverse(self.view_name)
        self.mock_qr_request['url'] = 'invalid-url'
        
        response = client.post(url, data=self.mock_qr_request)
        assert response.status_code == 400
        assert 'url' in response.json()['detail'].keys()
        assert response.json()['error_code'] == QRErrorCodes.INVALID_PARAMETERS


    def test_url_qr_error_response_format(self, client):
        """에러 응답 형식 테스트"""
        url = reverse(self.view_name)
        
        # 잘못된 URL로 테스트
        self.mock_qr_request['url'] = 'invalid-url'
        response = client.post(url, data=self.mock_qr_request)
        
        assert response.status_code == 400
        assert 'detail' in response.json()
        assert 'error_code' in response.json()

        
class TestQRTextEndpoint(QrTestBase):
    view_name = 'qr:qr_text_v1'
    mock_qr_request = {
        "text": "Hello, World!",
        "style": QRStyles.SQUARE_MODULE.value,
        "fill_color": "black",
        "back_color": "white",
        "color_mask": QRColorMasks.SOLID_FILL.value,
        "embedded_image_ratio": 0.2
    }
    
    def test_text_qr_generation_success(self, client):
        """기본 텍스트 QR 코드 생성 테스트"""
        url = reverse(self.view_name)
        response = client.post(url, data=self.mock_qr_request)
        self._validate_qr_response(response)

    def test_text_qr_missing_parameters(self, client):
        """필수 파라미터 누락 테스트"""
        url = reverse(self.view_name)
        response = client.post(url, data={})
