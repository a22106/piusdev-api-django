# qr/utils/qr_utils.py
from enum import Enum
from io import BytesIO
import logging
import urllib.parse
from PIL import Image, ImageColor

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


def _convert_color_to_rgb(color: str) -> tuple:
    """
    Convert color string to RGB tuple.
    Supports color names ('red', 'blue') and hex values ('#FF0000').
    """
    try:
        # ImageColor.getrgb는 'red', '#FF0000' 같은 색상명을 RGB 튜플로 변환
        return ImageColor.getrgb(color)
    except Exception as e:
        logger.error(f"Error converting color {color}: {e}")
        # 기본값으로 검정색 반환
        return (0, 0, 0)


def create_qr_code(
    data: str, version: int = None,
    error_correction: int = ERROR_CORRECT_L,
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
            error_correction=ERROR_CORRECT_H if embedded_image else error_correction,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)  # fit=True: QR code Version(size)를 자동으로 조절

        module_drawer = _get_module_drawer(style)
        color_mask_instance = _get_color_mask(color_mask)

        # 색상 문자열을 RGB 튜플로 변환
        fill_color_rgb = _convert_color_to_rgb(fill_color)
        back_color_rgb = _convert_color_to_rgb(back_color)

        color_mask_instance.back_color = back_color_rgb
        color_mask_instance.front_color = fill_color_rgb

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask_instance,
            embeded_image=embedded_image,
            embeded_image_ratio=embedded_image_ratio if embedded_image else 0,
        )

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception as e:
        logger.error(f"Error creating QR Code: {e}")
        raise


def generate_url_qr(
    url: str,
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    Generate a QR code for a URL.

    Args:
        url (str): The URL to encode in the QR code.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    return create_qr_code(
        url,
        style=style,
        fill_color=fill_color,
        back_color=back_color,
        color_mask=color_mask,
        embedded_image=embedded_image,
        embedded_image_ratio=embedded_image_ratio
    )


def generate_email_qr(
    email: str, subject: str = "", body: str = "",
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
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

    return create_qr_code(
        mailto,
        style=style,
        fill_color=fill_color,
        back_color=back_color,
        color_mask=color_mask,
        embedded_image=embedded_image,
        embedded_image_ratio=embedded_image_ratio
    )


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
        error_correction=ERROR_CORRECT_H if embedded_image else ERROR_CORRECT_L,
        embedded_image=embedded_image,
        embedded_image_ratio=embedded_image_ratio
    )


def generate_phone_qr(
    phone_number: str,
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    Generate a QR code for a phone number.

    :param phone_number: (+)1234567890 +는 필요하지 않음

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    tel = f"tel:{phone_number}"
    return create_qr_code(tel,
        style=style,
        fill_color=fill_color,
        back_color=back_color,
        color_mask=color_mask,
        embedded_image=embedded_image,
        embedded_image_ratio=embedded_image_ratio
    )


def generate_vcard_qr(
    first_name: str,
    last_name: str,
    vcard_mobile: str = "",
    vcard_email: str = "",
    vcard_url: str = "",
    organization: str = "",
    job_title: str = "",
    fax: str = "",
    address: str = "",
    zip: str = "",
    country: str = "",
    note: str = "",
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25) -> bytes:
    # VCard 생성 로직
    vcard_data = {
        "first_name": first_name,
        "last_name": last_name,
        "vcard_mobile": vcard_mobile,
        "vcard_email": vcard_email,
        "vcard_url": vcard_url,
        "organization": organization,
        "job_title": job_title,
        "fax": fax,
        "address": address,
        "zip": zip,
        "country": country,
        "note": note,
    }
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
            vcard,
            style=style,
            fill_color=fill_color,
            back_color=back_color,
            color_mask=color_mask,
            embedded_image=embedded_image,
            embedded_image_ratio=embedded_image_ratio
        )
    except Exception as e:
        logger.error(f"Error creating VCard QR Code: {e}")
        raise


def generate_wifi_qr(ssid: str, password: str, encryption: str = "WPA", hidden: bool = False,
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
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
        if hidden:
            wifi += "H:true;"

        return create_qr_code(wifi, version=2,
            style=style,
            fill_color=fill_color,
            back_color=back_color,
            color_mask=color_mask,
            embedded_image=embedded_image,
            embedded_image_ratio=embedded_image_ratio
        )
    except Exception as e:
        logger.error(f"Error creating WiFi QR Code: {e}")
        raise


def generate_sms_qr(phone_number: str, message: str,
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    Generate a QR code for an SMS message.

    Args:
        phone_number (str): The phone number.
        message (str): The SMS message.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    sms = f"SMSTO:{phone_number}:{message}"
    return create_qr_code(sms,
        style=style,
        fill_color=fill_color,
        back_color=back_color,
        color_mask=color_mask,
        embedded_image=embedded_image,
        embedded_image_ratio=embedded_image_ratio
    )


def generate_geo_qr(
    latitude: str, longitude: str, query: str = "", zoom: str = "0",
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    Geographic QR Code 생성

    Args:
        latitude (float): 위치 위도(latitude)
        longitude (float): 위치 경도(longitude)
        query (str, optional): 쿼리 파라미터, 예: 장소 이름. Defaults to ''.
        zoom (int, optional): 줌 레벨. Defaults to 0.

    Returns:
        bytes: The generated QR code image in PNG format.
    """
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        zoom = int(zoom)
        geo_uri = f"geo:{latitude},{longitude}"
        params = []
        if zoom > 0:
            params.append(f"z={zoom}")
        if query:
            params.append(f"q={query}")
        if params:
            geo_uri += "?" + "&".join(params)
        return create_qr_code(geo_uri,
            style=style,
            fill_color=fill_color,
            back_color=back_color,
            color_mask=color_mask,
            embedded_image=embedded_image,
            embedded_image_ratio=embedded_image_ratio
        )
    except Exception as e:
        logger.error(f"Error creating Geo QR Code: {e}")
        raise


def generate_event_qr(event_data: Dict[str, str],
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    Calendar Event QR Code 생성

    Args:
        event_data (Dict[str, str]): 이벤트 정보를 포함하는 딕셔너리.
            Required keys: summary, start_date, end_date, location, description

    Returns:
        bytes: 생성된 QR 코드 이미지(PNG 포맷)
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
        return create_qr_code(vcal,
            style=style,
            fill_color=fill_color,
            back_color=back_color,
            color_mask=color_mask,
            embedded_image=embedded_image,
            embedded_image_ratio=embedded_image_ratio
        )
    except Exception as e:
        logger.error(f"Error creating Event QR Code: {e}")
        raise


def generate_mecard_qr(
    name: str, reading: str, tel: str, email: str,
    memo: str = "", birthday: str = "", address: str = "", url: str = "", nickname: str = "",
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    MECARD QR Code 생성

    Args:
        mecard_data (Dict[str, str]): 연락처 정보를 포함하는 딕셔너리.
            필요한 키: name, reading, tel, email, memo, birthday, address, url, nickname

    Returns:
        bytes: 생성된 QR 코드 이미지(PNG 포맷)
    """
    try:
        mecard = "MECARD:"
        if name:
            mecard += f"N:{name};"
        if reading:
            mecard += f"SOUND:{reading};"
        if tel:
            mecard += f"TEL:{tel};"
        if email:
            mecard += f"EMAIL:{email};"
        if memo:
            mecard += f"NOTE:{memo};"
        if birthday:
            mecard += f"BDAY:{birthday};"
        if address:
            mecard += f"ADR:{address};"
        if url:
            mecard += f"URL:{url};"
        if nickname:
            mecard += f"NICKNAME:{nickname};"
        mecard += ";"
        return create_qr_code(mecard,
            style=style,
            fill_color=fill_color,
            back_color=back_color,
            color_mask=color_mask,
            embedded_image=embedded_image,
            embedded_image_ratio=embedded_image_ratio
        )
    except Exception as e:
        logger.error(f"Error creating MECARD QR Code: {e}")
        raise


def generate_whatsapp_qr(phone_number: str, message: str = "",
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    WhatsApp QR Code 생성

    Args:
        phone_number (str): 수신자의 전화번호(international format).
        message (str, optional): 보낼 메시지. Defaults to ''.

    Returns:
        bytes: 생성된 QR 코드 이미지(PNG 포맷)
    """
    try:
        whatsapp_uri = f"https://wa.me/{phone_number}"
        if message:
            query_params = {"text": message}
            encoded_params = urllib.parse.urlencode(query_params)
            whatsapp_uri += f"?{encoded_params}"
        return create_qr_code(whatsapp_uri,
            style=style,
            fill_color=fill_color,
            back_color=back_color,
            color_mask=color_mask,
            embedded_image=embedded_image,
            embedded_image_ratio=embedded_image_ratio
        )
    except Exception as e:
        logger.error(f"Error creating WhatsApp QR Code: {e}")
        raise


def generate_bitcoin_qr(
    address: str, amount: float = None, label: str = "", message: str = "",
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    Bitcoin QR Code 생성

    Args:
        address (str): 비트코인 주소.
        amount (float, optional): BTC 금액. Defaults to None.
        label (str, optional): 주소에 대한 라벨. Defaults to ''.
        message (str, optional): 결제에 대한 메시지. Defaults to ''.

    Returns:
        bytes: 생성된 QR 코드 이미지(PNG 포맷)
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
        return create_qr_code(bitcoin_uri,
            style=style,
            fill_color=fill_color,
            back_color=back_color,
            color_mask=color_mask,
            embedded_image=embedded_image,
            embedded_image_ratio=embedded_image_ratio
        )
    except Exception as e:
        logger.error(f"Error creating Bitcoin QR Code: {e}")
        raise
