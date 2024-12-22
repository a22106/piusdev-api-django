from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

def qr_swagger_decorator(operation_id, required_params):
    """QR코드 생성 엔드포인트에 사용되는 Swagger 데코레이터"""
    def decorator(func):
        common_properties = {
            'style': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='QR code style (SQUARE_MODULE, GAPPED_SQUARE_MODULE, CIRCLE_MODULE, ROUNDED_MODULE, HORIZONTAL_BARS, VERTICAL_BARS)',
                default='SQUARE_MODULE'
            ),
            'fill_color': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='QR code pattern color',
                default='black'
            ),
            'back_color': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='QR code background color',
                default='white'
            ),
            'color_mask': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Color mask type (SOLID_FILL, RADIAL_GRADIANT, SQUARE_GRADIANT, HORIZONTAL_GRADIANT, VERTICAL_GRADIANT)',
                default='SOLID_FILL'
            ),
            'embedded_image': openapi.Schema(
                type=openapi.TYPE_FILE,
                description='Image to embed in QR code'
            ),
            'embedded_image_ratio': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description='Size ratio of embedded image (0.1-0.5)',
                default=0.2
            ),
        }

        return swagger_auto_schema(
            operation_id=operation_id,
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={**required_params, **common_properties},
                required=list(required_params.keys())
            ),
            responses={
                200: openapi.Response("QR Code Image (PNG)"),
                400: openapi.Response("Bad Request"),
                500: openapi.Response("Server Error"),
            },
        )(func)
    return decorator
