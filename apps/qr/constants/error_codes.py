from enum import Enum

class QRErrorCodes(str, Enum):
    """QR 코드 생성 관련 에러 코드 정의"""
    INVALID_PARAMETERS = 'QR_INVALID_PARAMETERS'
    INVALID_IMAGE = 'QR_INVALID_IMAGE'
    GENERATION_FAILED = 'QR_GENERATION_FAILED'
    INVALID_URL = 'QR_INVALID_URL'
    INVALID_EMAIL = 'QR_INVALID_EMAIL'
    INVALID_PHONE = 'QR_INVALID_PHONE'
    INVALID_WIFI = 'QR_INVALID_WIFI'
    INVALID_VCARD = 'QR_INVALID_VCARD'
    INVALID_EVENT = 'QR_INVALID_EVENT'
    INVALID_GEO = 'QR_INVALID_GEO'
    INVALID_BITCOIN = 'QR_INVALID_BITCOIN'
    INTERNAL_ERROR = 'QR_INTERNAL_ERROR'
    INVALID_COLOR = 'QR_INVALID_COLOR'

class QRErrorMessages(dict):
    """에러 코드별 메시지 정의"""
    _messages = {
        QRErrorCodes.INVALID_PARAMETERS: "Wrong parameters were passed.",
        QRErrorCodes.INVALID_IMAGE: "Wrong image format.",
        QRErrorCodes.GENERATION_FAILED: "Failed to generate QR code.",
        QRErrorCodes.INVALID_URL: "Wrong URL format.",
        QRErrorCodes.INVALID_EMAIL: "Wrong email format.",
        QRErrorCodes.INVALID_PHONE: "Wrong phone number format.",
        QRErrorCodes.INVALID_WIFI: "Wrong WiFi settings.",
        QRErrorCodes.INVALID_VCARD: "Wrong VCard information.",
        QRErrorCodes.INVALID_EVENT: "Wrong event information.",
        QRErrorCodes.INVALID_GEO: "Wrong location information.",
        QRErrorCodes.INVALID_BITCOIN: "Wrong Bitcoin information.",
        QRErrorCodes.INTERNAL_ERROR: "Internal server error occurred.",
    }

    @classmethod
    def get_message(cls, error_code: QRErrorCodes) -> str:
        """에러 코드에 해당하는 메시지 반환"""
        return cls._messages.get(error_code, "An unknown error occurred.") 