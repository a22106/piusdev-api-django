import qrcode
from io import BytesIO
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def generate_qr_image(qr_text: str) -> HttpResponse:
    """
    Generates a QR code image from the provided text.

    Args:
        qr_text (str): The text to encode in the QR code.

    Returns:
        HttpResponse: An HTTP response containing the QR code image in PNG format.
    """
    logger.info(f"Generating QR Code for text: {qr_text}")

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

    return HttpResponse(buffer.getvalue(), content_type="image/png")