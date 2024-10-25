import qrcode
from io import BytesIO
from django.http import HttpResponse
import logging
from typing import Optional, TypedDict

class PhoneDict(TypedDict, total=False):
    WORK: str
    HOME: str
    MOBILE: str

class AddressDict(TypedDict, total=False):
    HOME: str
    WORK: str

class UrlDict(TypedDict, total=False):
    WORK: str
    PERSONAL: str
    
class LabelDict(TypedDict, total=False):
    HOME: str
    WORK: str

logger = logging.getLogger(__name__)


def simple_qrcode(text):
    img = qrcode.make(text)
    img.save("qrcode.png")
    return img


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


def vcard_text(
    first_name: str,
    last_name: str,
    email: str,
    phone: Optional[PhoneDict] = None,
    org: Optional[str] = None,
    title: Optional[str] = None,
    address: Optional[AddressDict] = None,
    label: Optional[LabelDict] = None,
    url: Optional[UrlDict] = None,
    note: Optional[str] = None,   
):
    """vCard text generator

    Args:
        first_name (str): First name
        last_name (str): Last name
        email (str): Email address
        phone (Optional[PhoneDict], optional): Phone numbers. Defaults to None.
        org (Optional[str], optional): Organization. Defaults to None.
        title (Optional[str], optional): Title. Defaults to None.
        department (Optional[str], optional): Department. Defaults to None.
        address (Optional[AddressDict], optional): Addresses. Defaults to None.
        label (Optional[LabelDict], optional): Label for address. Defaults to None.
        url (Optional[UrlDict], optional): URLs. Defaults to None.
        note (Optional[str], optional): Note. Defaults to None.

    Returns:
        str: vCard formatted text
    """
    vcard_text = f"FN:{first_name} {last_name}\nEMAIL:{email}"
    
    if phone:
        for phone_type, number in phone.items():
            vcard_text += f"\nTEL;TYPE={phone_type}:{number}"
    
    if org:
        vcard_text += f"\nORG:{org}"
    if title:
        vcard_text += f"\nTITLE:{title}"
    
    if address:
        for addr_type, addr in address.items():
            vcard_text += f"\nADR;TYPE={addr_type}:{addr}"
    
    if label:
        for label_type, label_text in label.items():
            vcard_text += f"\nLABEL;TYPE={label_type}:{label_text}"
    
    if url:
        for url_type, link in url.items():
            vcard_text += f"\nURL;TYPE={url_type}:{link}"
    
    if note:
        vcard_text += f"\nNOTE:{note}"
    
    return vcard_text


def vcard(qr_text: str) -> HttpResponse:
    """
    Generates a QR code image with a vCard encoded in the QR code.

    Args:
        qr_text (str): The vCard text to encode in the QR code.

    Returns:
        HttpResponse: An HTTP response containing the QR code image in PNG format.
    """
    vcard_img = qrcode.make(f"BEGIN:VCARD\n{qr_text}\nEND:VCARD")
    vcard_img.save("vcard.png")
    return generate_qr_image(qr_text)


if __name__ == "__main__":
    print(
        vcard(
            vcard_text(
                "Byeonggong",
                "Hwang",
                "bk22106@gmail.com",
                phone={"MOBILE": "+821099473728"},
                org="Mapsea",
                department="Research & Development",
                title="Senior Research Engineer",
                address={"HOME": "96, Jayang-ro 18-gil, Gwangjin-gu, Seoul, Republic of Korea"},
                label={"WORK": "Seoul, Republic of Korea"},
                url={"WORK": "https://www.mapsea.com"},
                note="Software Engineer",
            )
        )
    )
