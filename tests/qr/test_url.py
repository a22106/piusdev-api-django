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
class TestQRUrlEndpoint:
    def _validate_qr_response(self, response):
        """QR 코드 응답 검증을 위한 헬퍼 메서드"""
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/png'
        
        # 응답이 유효한 이미지인지 확인
        image = Image.open(BytesIO(response.content))
        assert image.format == 'PNG'

    def test_url_qr_generation_success(self, client, mock_qr_url_request):
        """기본 URL QR 코드 생성 테스트"""
        url = reverse('qr:qr_url_v1')
        response = client.post(url, data=mock_qr_url_request)
        self._validate_qr_response(response)

    def test_url_qr_missing_url(self, client, common_params):
        """URL 파라미터 누락 테스트"""
        url = reverse('qr:qr_url_v1')
        response = client.post(url, data=common_params)
        assert response.status_code == 400
        assert 'url' in response.json()

    def test_url_qr_invalid_url(self, client, common_params):
        """잘못된 URL 형식 테스트"""
        url = reverse('qr:qr_url_v1')
        data = {
            "url": "not_a_valid_url",
            **common_params
        }
        response = client.post(url, data=data)
        assert response.status_code == 400
        assert 'url' in response.json()

    def test_url_qr_invalid_style(self, client, mock_qr_url_request):
        """잘못된 스타일 파라미터 테스트"""
        url = reverse('qr:qr_url_v1')
        mock_qr_url_request['style'] = 'INVALID_STYLE'
        response = client.post(url, data=mock_qr_url_request)
        assert response.status_code == 400
        assert 'style' in response.json()

    def test_url_qr_invalid_color_mask(self, client, mock_qr_url_request):
        """잘못된 컬러 마스크 테스트"""
        url = reverse('qr:qr_url_v1')
        mock_qr_url_request['color_mask'] = 'INVALID_MASK'
        response = client.post(url, data=mock_qr_url_request)
        assert response.status_code == 400
        assert 'color_mask' in response.json()

    def test_url_qr_invalid_image_ratio(self, client, mock_qr_url_request):
        """잘못된 이미지 비율 테스트"""
        url = reverse('qr:qr_url_v1')
        mock_qr_url_request['embedded_image_ratio'] = 0.6  # 허용 범위 초과
        response = client.post(url, data=mock_qr_url_request)
        assert response.status_code == 400
        assert 'embedded_image_ratio' in response.json()

    def test_url_qr_with_different_styles(self, client, mock_qr_url_request):
        """다양한 스타일 테스트"""
        url = reverse('qr:qr_url_v1')
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
        url = reverse('qr:qr_url_v1')
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
        url = reverse('qr:qr_url_v1')
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

    # def test_style_variations(self):
    #     """다양한 스타일 테스트"""
    #     url = reverse('qr:qr_text_v1')
    #     styles = [
    #         "SQUARE_MODULE",
    #         "GAPPED_SQUARE_MODULE",
    #         "CIRCLE_MODULE",
    #         "ROUNDED_MODULE",
    #         "HORIZONTAL_BARS",
    #         "VERTICAL_BARS"
    #     ]
        
    #     for style in styles:
    #         data = {
    #             "text": "Style Test",
    #             **self.common_params,
    #             "style": style
    #         }
    #         response = client.post(url, data=data)
    #         self.assertEqual(response.status_code, 200) 