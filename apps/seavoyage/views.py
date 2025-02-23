import seavoyage as sv
import logging
import sys
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import CoordinateSerializer, SeaRouteResponseSerializer
from .models import SeaRoute

# 로거 설정
logger = logging.getLogger(__name__)

class SeavoyageHelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})

class SeavoyageView(APIView):
    @swagger_auto_schema(
        operation_description="해상 경로를 계산합니다",
        query_serializer=CoordinateSerializer,
        responses={200: SeaRouteResponseSerializer}
    )
    def get(self, request: Request):
        try:
            serializer = CoordinateSerializer(data=request.query_params)
            
            if not serializer.is_valid():
                logger.error(f"유효하지 않은 입력 데이터: {serializer.errors}")
                return Response(serializer.errors, status=400)
            
            # 입력값 로깅
            logger.info(f"경로 계산 시작 - 출발: {serializer.validated_data['origin']}, 도착: {serializer.validated_data['destination']}, 거리 단위: {serializer.validated_data['units']}")
            
            m_network = sv.get_m_network_5km()
            
            origin: tuple[float, float] = tuple(map(float, serializer.validated_data['origin'].split(',')))
            origin = (origin[1], origin[0]) # 입력은 위도, 경도 순으로 들어오지만 좌표계에서는 경도, 위도 순으로 들어가야 함
            destination: tuple[float, float] = tuple(map(float, serializer.validated_data['destination'].split(',')))
            destination = (destination[1], destination[0]) # 입력은 위도, 경도 순으로 들어오지만 좌표계에서는 경도, 위도 순으로 들어가야 함
            
            result = sv.seavoyage(
                origin,
                destination,
                M=m_network
            )
            
            # save_to_db 파라미터로 저장 여부 결정 (기본값: False)
            save_to_db = request.query_params.get('save_to_db', '').lower() == 'true'
            
            if save_to_db:
                route = SeaRoute.objects.create(
                    origin=serializer.validated_data['origin'],
                    destination=serializer.validated_data['destination'],
                    distance=result['properties']['length'],
                    units=serializer.validated_data['units'],
                    geojson=result['geometry']
                )
                response_data = SeaRouteResponseSerializer(route).data
            else:
                # DB 저장 없이 결과 반환
                response_data = {
                    'origin': serializer.validated_data['origin'],
                    'destination': serializer.validated_data['destination'],
                    'distance': result['properties']['length'],
                    'units': serializer.validated_data['units'],
                    'geojson': result['geometry']
                }
            
            return Response(response_data)
                
        except Exception as e:
            logger.error(f"예상치 못한 오류 발생: {str(e)}", exc_info=True)
            return Response({"error": str(e)}, status=500)
