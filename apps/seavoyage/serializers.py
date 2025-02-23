import re
from rest_framework import serializers

from apps.seavoyage.constants import DistanceUnit
from .models import SeaRoute

class CoordinateSerializer(serializers.Serializer):
    """좌표 입력을 위한 Serializer"""
    origin = serializers.CharField(
        help_text="출발지 좌표 (위도(latitude), 경도(longitude) 형식)",
        required=True
    )
    destination = serializers.CharField(
        help_text="도착지 좌표 (위도(latitude), 경도(longitude) 형식)",
        required=True
    )
    
    units = serializers.ChoiceField(
        choices=DistanceUnit.values(),
        help_text=f"거리 단위",
        required=False,
        default="nm"
    )
    
    # 선택적 DB 저장 파라미터 추가
    save_to_db = serializers.BooleanField(
        help_text="계산된 경로를 DB에 저장할지 여부",
        required=False,
        default=False
    )
    
    # validate
    def validate_origin(self, value):
        try:
            # 위경도 값 추출 및 범위 검증
            lat, lon = map(float, value.split(','))
            self.validate_latitude_range(lat)   
            self.validate_longitude_range(lon)
            return value
        except ValueError:
            raise serializers.ValidationError(f"The coordinate value is not a valid number format. input value: {value}")
        except Exception as e:
            raise serializers.ValidationError(f"Coordinate format validation error: {str(e)}")
    
    def validate_destination(self, value):
        return self.validate_origin(value)
    
    def validate_latitude_range(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError(f"The latitude must be between -90 and 90. input value: {value}")
        return value
    
    def validate_longitude_range(self, value):
        if not -180 <= value <= 180:
            raise serializers.ValidationError(f"The longitude must be between -180 and 180. input value: {value}")
        return value
    
    def validate_units(self, value):
        if value not in DistanceUnit.values():
            raise serializers.ValidationError(f"Invalid distance unit. input value: {value}")
        return value

class SeaRouteResponseSerializer(serializers.ModelSerializer):
    """해상 경로 응답을 위한 Serializer"""
    geojson = serializers.JSONField()
    
    class Meta:
        model = SeaRoute
        fields = ['origin', 'destination', 'distance', 'units', 'geojson']