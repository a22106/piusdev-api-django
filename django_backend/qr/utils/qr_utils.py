# qr/utils/qr_utils.py
from enum import Enum
from io import BytesIO
import logging
import urllib.parse
from PIL import Image

from typing import Dict, Type

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_H
from qrcode.main import QRCode
from qrcode.image.styledpil import StyledPilImage

# QR Code Styles
from qrcode.image.styles.moduledrawers.pil import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    HorizontalBarsDrawer,
    VerticalBarsDrawer,
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask,
    RadialGradiantColorMask,
    SquareGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask,
    ImageColorMask,
)


logger = logging.getLogger(__name__)


class QRStyles(Enum):
    SQUARE_MODULE = 1
    GAPPED_SQUARE_MODULE = 2
    CIRCLE_MODULE = 3
    ROUNDED_MODULE = 4
    HORIZONTAL_BARS = 5
    VERTICAL_BARS = 6


class QRColorMasks(Enum):
    SOLID_FILL = 1
    RADIAL_GRADIANT = 2
    SQUARE_GRADIANT = 3
    HORIZONTAL_GRADIANT = 4
    VERTICAL_GRADIANT = 5


def _get_module_drawer(style: Type[QRStyles]):
    style_map = {
        QRStyles.SQUARE_MODULE: SquareModuleDrawer(),
        QRStyles.GAPPED_SQUARE_MODULE: GappedSquareModuleDrawer(),
        QRStyles.CIRCLE_MODULE: CircleModuleDrawer(),
        QRStyles.ROUNDED_MODULE: RoundedModuleDrawer(),
        QRStyles.HORIZONTAL_BARS: HorizontalBarsDrawer(),
        QRStyles.VERTICAL_BARS: VerticalBarsDrawer(),
    }
    result = style_map.get(style, SquareModuleDrawer())
    return result


def _get_color_mask(mask_type: Type[QRColorMasks]):
    mask_map = {
        QRColorMasks.SOLID_FILL: SolidFillColorMask(),
        QRColorMasks.RADIAL_GRADIANT: RadialGradiantColorMask(),
        QRColorMasks.SQUARE_GRADIANT: SquareGradiantColorMask(),
        QRColorMasks.HORIZONTAL_GRADIANT: HorizontalGradiantColorMask(),
        QRColorMasks.VERTICAL_GRADIANT: VerticalGradiantColorMask(),
    }

    result = mask_map.get(mask_type, SolidFillColorMask())
    return result

def create_qr_code(
    data: str, version: int = None,
    error_correction=ERROR_CORRECT_L,
    fill_color: str = "black",
    back_color: str = "white",
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    try:
        qr = QRCode(
            version=version,
            error_correction=error_correction,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True) # fit=True: QR code Version(size)를 자동으로 조절

        module_drawer = _get_module_drawer(style)
        color_mask = _get_color_mask(color_mask)

        img = qr.make_image(
            image_factory=StyledPilImage,
            fill=fill_color,
            back_color=back_color,
            module_drawer=module_drawer,
            color_mask=color_mask,
            embeded_image=embedded_image,
            embeded_image_ratio=embedded_image_ratio,
        )

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception as e:
        logger.error(f"Error creating QR Code: {e}")
        raise


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


def generate_text_qr(
    text: str,
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    Generate a QR code for plain text.

    Args:
        text (str): The text to encode in the QR code.
        style (QRStyles): The style of the QR code.
        fill_color (str): Color of the QR code pattern.
        back_color (str): Background color.
        color_mask (QRColorMasks): Color mask type for gradient effects.
        embedded_image (PIL.Image): Optional image to embed in center of QR code.
        embedded_image_ratio (float): Size ratio of embedded image (0.1-0.5).

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    return create_qr_code(
        text,
        style=style,
        fill_color=fill_color,
        back_color=back_color,
        color_mask=color_mask,
        embedded_image=embedded_image,
        embedded_image_ratio=embedded_image_ratio
    )


def generate_phone_qr(phone_number: str) -> bytes:
    """
    Generate a QR code for a phone number.

    :param phone_number: (+)1234567890 +는 필요하지 않음

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    tel = f"tel:{phone_number}"
    return create_qr_code(tel)


def generate_vcard_qr(vcard_data: Dict[str, str]) -> bytes:
    """
    Generate a QR code for a VCard.

    Args:
        vcard_data (Dict[str, str]): A dictionary containing VCard information.
            Expected keys: first_name, last_name, email, mobile,
                           organization, title, address, label, url, note

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
        if vcard_data.get("birthday"):
            vcard += f"BDAY:{vcard_data.get('birthday')}\n"
        if vcard_data.get("vcard_email"):
            vcard += f"EMAIL:{vcard_data.get('vcard_email')}\n"
        if vcard_data.get("vcard_phone"):
            vcard += f"TEL;TYPE=VOICE:{vcard_data.get('vcard_phone')}\n"
        if vcard_data.get("vcard_mobile"):
            vcard += f"TEL;TYPE=CELL:{vcard_data.get('vcard_mobile')}\n"
        if vcard_data.get("organization"):
            vcard += f"ORG:{vcard_data.get('organization')}\n"
        if vcard_data.get("job_title"):
            vcard += f"TITLE:{vcard_data.get('job_title')}\n"
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
        encryption (str, optional): The encryption type ('WPA', 'WEP', 'none'). Defaults to "WPA".

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    try:
        if encryption.lower() == "none":
            wifi = f"WIFI:T:;S:{ssid};P:{password};;"
        else:
            wifi = f"WIFI:T:{encryption};S:{ssid};P:{password};;"

        return create_qr_code(wifi, version=2)
    except Exception as e:
        logger.error(f"Error creating WiFi QR Code: {e}")
        raise


def generate_sms_qr(phone_number: str, message: str) -> bytes:
    """
    Generate a QR code for an SMS message.

    Args:
        phone_number (str): The phone number.
        message (str): The SMS message.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    sms = f"SMSTO:{phone_number}:{message}"
    return create_qr_code(sms)


def generate_geo_qr(
    latitude: float, longitude: float, query: str = "", zoom: int = 0
) -> bytes:
    """
    Generate a QR code for a geographical location.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        query (str, optional): Query parameter, e.g., place name. Defaults to ''.
        zoom (int, optional): Zoom level. Defaults to 0.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    try:
        geo_uri = f"geo:{latitude},{longitude}"
        params = []
        if zoom > 0:
            params.append(f"z={zoom}")
        if query:
            params.append(f"q={query}")
        if params:
            geo_uri += "?" + "&".join(params)
        return create_qr_code(geo_uri)
    except Exception as e:
        logger.error(f"Error creating Geo QR Code: {e}")
        raise


def generate_event_qr(event_data: Dict[str, str]) -> bytes:
    """
    Generate a QR code for a calendar event.

    Args:
        event_data (Dict[str, str]): A dictionary containing event information.
            Expected keys: summary, start_date, end_date, location, description

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    try:
        vcal = "BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\n"
        vcal += f"SUMMARY:{event_data.get('summary', '')}\n"
        vcal += f"DTSTART:{event_data.get('start_date', '')}\n"
        vcal += f"DTEND:{event_data.get('end_date', '')}\n"
        if event_data.get("location"):
            vcal += f"LOCATION:{event_data.get('location')}\n"
        if event_data.get("description"):
            vcal += f"DESCRIPTION:{event_data.get('description')}\n"
        vcal += "END:VEVENT\nEND:VCALENDAR"
        return create_qr_code(vcal)
    except Exception as e:
        logger.error(f"Error creating Event QR Code: {e}")
        raise


def generate_mecard_qr(mecard_data: Dict[str, str]) -> bytes:
    """
    Generate a QR code in MECARD format.

    Args:
        mecard_data (Dict[str, str]): A dictionary containing contact information.
            Expected keys: name, reading, tel, email, memo, birthday, address, url, nickname

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    try:
        mecard = "MECARD:"
        if mecard_data.get("name"):
            mecard += f"N:{mecard_data.get('name')};"
        if mecard_data.get("reading"):
            mecard += f"SOUND:{mecard_data.get('reading')};"
        if mecard_data.get("tel"):
            mecard += f"TEL:{mecard_data.get('tel')};"
        if mecard_data.get("email"):
            mecard += f"EMAIL:{mecard_data.get('email')};"
        if mecard_data.get("memo"):
            mecard += f"NOTE:{mecard_data.get('memo')};"
        if mecard_data.get("birthday"):
            mecard += f"BDAY:{mecard_data.get('birthday')};"
        if mecard_data.get("address"):
            mecard += f"ADR:{mecard_data.get('address')};"
        if mecard_data.get("url"):
            mecard += f"URL:{mecard_data.get('url')};"
        if mecard_data.get("nickname"):
            mecard += f"NICKNAME:{mecard_data.get('nickname')};"
        mecard += ";"
        return create_qr_code(mecard)
    except Exception as e:
        logger.error(f"Error creating MECARD QR Code: {e}")
        raise


def generate_whatsapp_qr(phone_number: str, message: str = "") -> bytes:
    """
    Generate a QR code for a WhatsApp message.

    Args:
        phone_number (str): The recipient's phone number in international format.
        message (str, optional): The message to send. Defaults to ''.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    try:
        whatsapp_uri = f"https://wa.me/{phone_number}"
        if message:
            query_params = {"text": message}
            encoded_params = urllib.parse.urlencode(query_params)
            whatsapp_uri += f"?{encoded_params}"
        return create_qr_code(whatsapp_uri)
    except Exception as e:
        logger.error(f"Error creating WhatsApp QR Code: {e}")
        raise


def generate_bitcoin_qr(
    address: str, amount: float = None, label: str = "", message: str = ""
) -> bytes:
    """
    Generate a QR code for a Bitcoin payment.

    Args:
        address (str): The Bitcoin address.
        amount (float, optional): The amount in BTC. Defaults to None.
        label (str, optional): A label for the address. Defaults to ''.
        message (str, optional): A message for the payment. Defaults to ''.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    try:
        bitcoin_uri = f"bitcoin:{address}"
        params = []
        if amount is not None:
            params.append(f"amount={amount}")
        if label:
            params.append(f"label={label}")
        if message:
            params.append(f"message={message}")
        if params:
            bitcoin_uri += "?" + "&".join(params)
        return create_qr_code(bitcoin_uri)
    except Exception as e:
        logger.error(f"Error creating Bitcoin QR Code: {e}")
        raise
