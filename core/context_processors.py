from .models import SiteSettings


def site_settings(request):
    config = SiteSettings.objects.first()
    return {
        'site_title': config.title if config else 'QR Code Generator - PiusDev',
        'site_description': config.description if config else 'Generate various types of QR codes easily and quickly.',
        'site_keywords': config.keywords if config else 'QR Code, Generator, PiusDev',
    }