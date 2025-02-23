from enum import Enum

class QRStyles(str, Enum):
    """QR 코드 스타일 정의"""
    SQUARE_MODULE = 'SQUARE_MODULE'
    GAPPED_SQUARE_MODULE = 'GAPPED_SQUARE_MODULE'
    CIRCLE_MODULE = 'CIRCLE_MODULE'
    ROUNDED_MODULE = 'ROUNDED_MODULE'
    HORIZONTAL_BARS = 'HORIZONTAL_BARS'
    VERTICAL_BARS = 'VERTICAL_BARS'
    
    @classmethod
    def get_all_styles(cls):
        return [style.value for style in cls]

class QRColorMasks(str, Enum):
    """QR 코드 색상 마스크 정의"""
    SOLID_FILL = 'SOLID_FILL'
    RADIAL_GRADIANT = 'RADIAL_GRADIANT'
    SQUARE_GRADIANT = 'SQUARE_GRADIANT'
    HORIZONTAL_GRADIANT = 'HORIZONTAL_GRADIANT'
    VERTICAL_GRADIANT = 'VERTICAL_GRADIANT'
    
    @classmethod
    def get_all_color_masks(cls):
        return [mask.value for mask in cls]

class QREyeStyles(str, Enum):
    """QR 코드 Eye 스타일 정의"""
    SQUARE = 'SQUARE'
    CIRCLE = 'CIRCLE'
    ROUNDED = 'ROUNDED'

    @classmethod
    def get_all_eye_styles(cls):
        return [style.value for style in cls]

class WifiEncryption(str, Enum):
    """WiFi 암호화 방식 정의"""
    WPA = 'WPA'
    WEP = 'WEP'
    NONE = 'none' 