from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

import logging, qrcode
from io import BytesIO

logger = logging.getLogger(__name__)


def index(request):
    qr_text = "Hello World"
    if request.method == "POST":
        logger.info(f"POST request: {request.POST}")
        qr_text = request.POST.get("url")
    return render(request, "qr/index.html", {"qr_text": qr_text})

@require_http_methods(["POST"])
def qr_image(request):
    qr_text = request.POST.get("text", "Hello World")
    logger.info(f"QR Text: {qr_text}")
        
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)
    
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    return response
