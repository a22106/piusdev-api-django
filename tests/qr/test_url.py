from django.urls import reverse
from PIL import Image
from io import BytesIO
import pytest
from unittest.mock import patch, Mock

@pytest.fixture
def common_params():
    return {
        "style": "SQUARE_MODULE",
        "fill_color": "black",
        "back_color": "white",
        "color_mask": "SOLID_FILL",
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
    def _validate_qr_response(self, response):
        """QR 코드 응답 검증을 위한 헬퍼 메서드"""
        assert response.status_code == 200
        assert response.get('Content-Type') == 'image/png'
        
        # 응답이 유효한 이미지인지 확인
        image = Image.open(BytesIO(response.content))
        assert image.format == 'PNG'
        

@pytest.mark.django_db
class TestQRUrlEndpoint(QrTestBase):
    view_name = 'qr:qr_url_v1'
    def test_url_qr_generation_success(self, client, mock_qr_url_request):
        """기본 URL QR 코드 생성 테스트"""
        url = reverse(self.view_name)
        response = client.post(url, data=mock_qr_url_request)
        self._validate_qr_response(response)

    def test_url_qr_missing_parameters(self, client):
        """필수 파라미터 누락 테스트"""
        url = reverse(self.view_name)
        response = client.post(url, data={})
        
        assert response.status_code == 400
        assert response.json()['detail'] == 'Missing required parameters: url'
        assert response.json()['error_code'] == 'MISSING_PARAMETERS'

    def test_url_qr_invalid_parameters(self, client, mock_qr_url_request):
        """잘못된 파라미터 테스트"""
        url = reverse(self.view_name)
        mock_qr_url_request['embedded_image_ratio'] = 2.0  # 허용 범위 초과
        
        response = client.post(url, data=mock_qr_url_request)
        assert response.status_code == 400
        assert 'embedded_image_ratio' in response.json()['detail']
        assert response.json()['error_code'] == 'INVALID_PARAMETERS'

    def test_url_qr_invalid_style(self, client, mock_qr_url_request):
        """잘못된 스타일 파라미터 테스트"""
        url = reverse(self.view_name)
        mock_qr_url_request['style'] = 'INVALID_STYLE'
        response = client.post(url, data=mock_qr_url_request)
        assert response.status_code == 400
        assert 'style' in response.json()

    def test_url_qr_invalid_color_mask(self, client, mock_qr_url_request):
        """잘못된 컬러 마스크 테스트"""
        url = reverse(self.view_name)
        mock_qr_url_request['color_mask'] = 'INVALID_MASK'
        response = client.post(url, data=mock_qr_url_request)
        assert response.status_code == 400
        assert 'color_mask' in response.json()

    def test_url_qr_invalid_image_ratio(self, client, mock_qr_url_request):
        """잘못된 이미지 비율 테스트"""
        url = reverse(self.view_name)
        mock_qr_url_request['embedded_image_ratio'] = 0.6  # 허용 범위 초과
        response = client.post(url, data=mock_qr_url_request)
        assert response.status_code == 400
        assert 'embedded_image_ratio' in response.json()

    def test_url_qr_with_different_styles(self, client, mock_qr_url_request):
        """다양한 스타일 테스트"""
        url = reverse(self.view_name)
        styles = [
            "SQUARE_MODULE",
            "GAPPED_SQUARE_MODULE",
            "CIRCLE_MODULE",
            "ROUNDED_MODULE",
            "HORIZONTAL_BARS",
            "VERTICAL_BARS"
        ]
        
        for style in styles:
            mock_qr_url_request['style'] = style
            response = client.post(url, data=mock_qr_url_request)
            self._validate_qr_response(response)

    def test_url_qr_with_different_colors(self, client, mock_qr_url_request):
        """다양한 색상 조합 테스트"""
        url = reverse(self.view_name)
        color_tests = [
            {"fill_color": "red", "back_color": "white"},
            {"fill_color": "#FF0000", "back_color": "#FFFFFF"},
            {"fill_color": "rgb(255,0,0)", "back_color": "rgb(255,255,255)"}
        ]
        
        for colors in color_tests:
            mock_qr_url_request.update(colors)
            response = client.post(url, data=mock_qr_url_request)
            self._validate_qr_response(response)

    def test_url_qr_with_different_masks(self, client, mock_qr_url_request):
        """다양한 컬러 마스크 테스트"""
        url = reverse(self.view_name)
        masks = [
            "SOLID_FILL",
            "RADIAL_GRADIANT",
            "SQUARE_GRADIANT",
            "HORIZONTAL_GRADIANT",
            "VERTICAL_GRADIANT"
        ]
        
        for mask in masks:
            mock_qr_url_request['color_mask'] = mask
            response = client.post(url, data=mock_qr_url_request)
            self._validate_qr_response(response)

    def test_url_qr_error_response_format(self, client, mock_qr_url_request):
        """에러 응답 형식 테스트"""
        url = reverse(self.view_name)
        
        # 잘못된 URL로 테스트
        mock_qr_url_request['url'] = 'invalid-url'
        response = client.post(url, data=mock_qr_url_request)
        
        assert response.status_code == 400
        assert 'detail' in response.json()
        assert 'error_code' in response.json()
        
    @patch('apps.qr.views.generate_url_qr')
    def test_url_qr_generation_failure(self, mock_generate_qr, client, mock_qr_url_request):
        """QR 코드 생성 실패 테스트"""
        mock_generate_qr.return_value = None
        
        url = reverse(self.view_name)
        response = client.post(url, data=mock_qr_url_request)
        
        assert response.status_code == 500
        assert response.json()['detail'] == 'An unexpected error occurred while generating the QR Code.'
        assert response.json()['error_code'] == 'INTERNAL_SERVER_ERROR'