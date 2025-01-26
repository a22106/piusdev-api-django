from enum import Enum

class QRStyles(str, Enum):
    """QR 코드 스타일 정의"""
    SQUARE_MODULE = 'SQUARE_MODULE'
    GAPPED_SQUARE_MODULE = 'GAPPED_SQUARE_MODULE'
    CIRCLE_MODULE = 'CIRCLE_MODULE'
    ROUNDED_MODULE = 'ROUNDED_MODULE'
    HORIZONTAL_BARS = 'HORIZONTAL_BARS'
    VERTICAL_BARS = 'VERTICAL_BARS'

class QRColorMasks(str, Enum):
    """QR 코드 색상 마스크 정의"""
    SOLID_FILL = 'SOLID_FILL'
    RADIAL_GRADIANT = 'RADIAL_GRADIANT'
    SQUARE_GRADIANT = 'SQUARE_GRADIANT'
    HORIZONTAL_GRADIANT = 'HORIZONTAL_GRADIANT'
    VERTICAL_GRADIANT = 'VERTICAL_GRADIANT'

class QREyeStyles(str, Enum):
    """QR 코드 Eye 스타일 정의"""
    SQUARE = 'SQUARE'
    CIRCLE = 'CIRCLE'
    ROUNDED = 'ROUNDED'

class WifiEncryption(str, Enum):
    """WiFi 암호화 방식 정의"""
    WPA = 'WPA'
    WEP = 'WEP'
    NONE = 'none' 