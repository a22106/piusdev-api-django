from apps.qr.constants.enums import QRStyles, QRColorMasks


def site_settings(request):
    return {
        'SITE_TITLE': 'QR Code Generator - PiusDev',
        'SITE_DESCRIPTION': 'Generate various types of QR codes easily and quickly.',
        'SITE_KEYWORDS': 'QR Code, Generator, PiusDev',
    }

def qr_styles(request):
    return {
        'QR_STYLES': [(style.value, style.name) for style in QRStyles],
        'QR_COLOR_MASKS': [(mask.value, mask.name) for mask in QRColorMasks],
    }