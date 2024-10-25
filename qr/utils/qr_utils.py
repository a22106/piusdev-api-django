# qr/utils/qr_utils.py
import qrcode
from io import BytesIO
import logging
from typing import Dict

logger = logging.getLogger(__name__)


def create_qr_code(
    data: str, version: int = 1, error_correction=qrcode.constants.ERROR_CORRECT_L
) -> bytes:
    """
    Create a QR code image from the given data.

    Args:
        data (str): The data to encode in the QR code.
        version (int, optional): The version of the QR code. Defaults to 1.
        error_correction: The error correction level. Defaults to ERROR_CORRECT_L.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def generate_url_qr(url: str) -> bytes:
    """
    Generate a QR code for a URL.

    Args:
        url (str): The URL to encode in the QR code.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    return create_qr_code(url)


def generate_email_qr(email: str, subject: str = "", body: str = "") -> bytes:
    """
    Generate a QR code for an Email.

    Args:
        email (str): The recipient email address.
        subject (str, optional): The email subject. Defaults to "".
        body (str, optional): The email body. Defaults to "".

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    mailto = f"mailto:{email}"
    params = []
    if subject:
        params.append(f"subject={subject}")
    if body:
        params.append(f"body={body}")
    if params:
        mailto += "?" + "&".join(params)

    return create_qr_code(mailto)


def generate_text_qr(text: str) -> bytes:
    """
    Generate a QR code for plain text.

    Args:
        text (str): The text to encode in the QR code.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    return create_qr_code(text)


def generate_phone_qr(phone: str) -> bytes:
    """
    Generate a QR code for a phone number.

    Args:
        phone (str): The phone number to encode in the QR code.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    tel = f"tel:{phone}"
    return create_qr_code(tel)


def generate_vcard_qr(vcard_data: Dict[str, str]) -> bytes:
    """
    Generate a QR code for a VCard.

    Args:
        vcard_data (Dict[str, str]): A dictionary containing VCard information.
            Expected keys: first_name, last_name, vcard_email, vcard_mobile,
                           organization, title, address, label, vcard_url, note

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    try:
        vcard = "BEGIN:VCARD\nVERSION:3.0\n"
        vcard += (
            f"N:{vcard_data.get('last_name', '')};{vcard_data.get('first_name', '')}\n"
        )
        vcard += (
            f"FN:{vcard_data.get('first_name', '')} {vcard_data.get('last_name', '')}\n"
        )
        if vcard_data.get("vcard_email"):
            vcard += f"EMAIL:{vcard_data.get('vcard_email')}\n"
        if vcard_data.get("vcard_mobile"):
            vcard += f"TEL;TYPE=CELL:{vcard_data.get('vcard_mobile')}\n"
        if vcard_data.get("organization"):
            vcard += f"ORG:{vcard_data.get('organization')}\n"
        if vcard_data.get("title"):
            vcard += f"TITLE:{vcard_data.get('title')}\n"
        if vcard_data.get("address"):
            vcard += f"ADR;TYPE=HOME:;;{vcard_data.get('address')};;;;\n"
        if vcard_data.get("label"):
            vcard += f"LABEL;TYPE=HOME:{vcard_data.get('label')}\n"
        if vcard_data.get("vcard_url"):
            vcard += f"URL:{vcard_data.get('vcard_url')}\n"
        if vcard_data.get("note"):
            vcard += f"NOTE:{vcard_data.get('note')}\n"
        vcard += "END:VCARD"

        return create_qr_code(
            vcard, version=3, error_correction=qrcode.constants.ERROR_CORRECT_Q
        )
    except Exception as e:
        logger.error(f"Error creating VCard QR Code: {e}")
        raise


def generate_wifi_qr(ssid: str, password: str, encryption: str = "WPA") -> bytes:
    """
    Generate a QR code for WiFi configuration.

    Args:
        ssid (str): The WiFi SSID.
        password (str): The WiFi password.
        encryption (str, optional): The encryption type ('WPA', 'WEP', 'nopass'). Defaults to "WPA".

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    try:
        if encryption.lower() == "nopass":
            wifi = f"WIFI:T:;S:{ssid};P:{password};;"
        else:
            wifi = f"WIFI:T:{encryption};S:{ssid};P:{password};;"

        return create_qr_code(wifi, version=2)
    except Exception as e:
        logger.error(f"Error creating WiFi QR Code: {e}")
        raise
