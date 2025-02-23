from rest_framework.response import Response
from ..constants.error_codes import QRErrorCodes, QRErrorMessages

def create_error_response(error_code: QRErrorCodes, status_code: int = 400, **additional_data) -> Response:
    """
    표준화된 에러 응답을 생성하는 유틸리티 함수
    
    Args:
        error_code (QRErrorCodes): 에러 코드
        status_code (int): HTTP 상태 코드
        additional_data (dict): 추가적인 에러 데이터
    """
    response_data = {
        'error_code': error_code,
        'message': QRErrorMessages.get_message(error_code),
        **additional_data
    }
    
    return Response(response_data, status=status_code) 