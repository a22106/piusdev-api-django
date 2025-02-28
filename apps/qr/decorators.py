from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from apps.qr.constants.enums import QRStyles, QRColorMasks

def qr_swagger_decorator(operation_id, serializer_class, tags=["QR Code"], description=None):
    """QR코드 생성 엔드포인트에 사용되는 Swagger 데코레이터"""
    if description is None:
        description = ""
    description += f"""
    - `style`: {QRStyles.get_all_styles()}
    - `color_mask`: {QRColorMasks.get_all_color_masks()}
    - `fill_color`: #000000 or black or rgb(0,0,0)
    - `back_color`: #FFFFFF or white or rgb(255,255,255)
    - `embedded_image`: Image file
    - `embedded_image_ratio`: 0.2 (0.1-0.5)
    """
    def decorator(func):
        # 시리얼라이저의 필드들을 스키마로 변환
        serializer_fields = {}
        for field_name, field in serializer_class().get_fields().items():
            if isinstance(field, serializers.ChoiceField):
                schema = openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=field.choices,
                    default=field.default if field.default != serializers.empty else None
                )
            elif isinstance(field, serializers.BooleanField):
                schema = openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    default=field.default if field.default != serializers.empty else None
                )
            elif isinstance(field, serializers.IntegerField):
                schema = openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    default=field.default if field.default != serializers.empty else None
                )
            elif isinstance(field, serializers.FloatField):
                schema = openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    default=field.default if field.default != serializers.empty else None
                )
            elif isinstance(field, serializers.ImageField):
                schema = openapi.Schema(
                    type=openapi.TYPE_FILE,
                )
            else:
                schema = openapi.Schema(
                    type=openapi.TYPE_STRING,
                    default=field.default if field.default != serializers.empty else None
                )
            serializer_fields[field_name] = schema

        common_properties = {
            'style': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='QR code style  {}'.format(', '.join([style.name for style in QRStyles])),
                default=QRStyles.SQUARE_MODULE.value
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
                description='Color mask type {}'.format(', '.join([mask.name for mask in QRColorMasks])),
                default=QRColorMasks.SOLID_FILL.value
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
            operation_description=description,
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={**serializer_fields, **common_properties},
                required=[field_name for field_name, field in serializer_class().get_fields().items() 
                         if field.required]
            ),
            tags=tags,
            responses={
                200: openapi.Response("QR Code Image (PNG)"),
                400: openapi.Response("Bad Request"),
                500: openapi.Response("Server Error"),
            },
        )(func)
    return decorator
