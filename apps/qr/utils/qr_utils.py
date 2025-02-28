# qr/utils/qr_utils.py
from enum import Enum
from io import BytesIO
import logging
import traceback
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
from apps.qr.serializers import BaseQRSerializer

from ..constants import QRStyles, QRColorMasks, QREyeStyles


logger = logging.getLogger(__name__)

def _get_eye_style(style: Type[QREyeStyles]):
    style_map = {
        QREyeStyles.SQUARE: None,
        QREyeStyles.CIRCLE: CircleModuleDrawer(),
        QREyeStyles.ROUNDED: RoundedModuleDrawer(),
    }
    result = style_map.get(style, None)
    return result


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
        QRColorMasks.SOLID_FILL: SolidFillColorMask,
        QRColorMasks.RADIAL_GRADIANT: RadialGradiantColorMask,
        QRColorMasks.SQUARE_GRADIANT: SquareGradiantColorMask,
        QRColorMasks.HORIZONTAL_GRADIANT: HorizontalGradiantColorMask,
        QRColorMasks.VERTICAL_GRADIANT: VerticalGradiantColorMask,
    }

    result = mask_map.get(mask_type, SolidFillColorMask)
    return result


def _convert_color_to_rgb(color: str) -> tuple:
    """문자열 색상을 RGB 튜플로 변환. 색상명 ('red', 'blue')과 16진수 값 ('#FF0000')을 지원."""
    # ImageColor.getrgb는 'red', '#FF0000' 같은 색상명을 RGB 튜플로 변환

    return ImageColor.getrgb(color)


def create_qr_code(
    data: str, version: int = None,
    error_correction: int = ERROR_CORRECT_L,
    eye_style: Type[QREyeStyles] = None,
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

        # 색상을 RGB 튜플로 변환
        fill_rgb = _convert_color_to_rgb(fill_color)
        back_rgb = _convert_color_to_rgb(back_color)

        mask_class = _get_color_mask(color_mask)

        # Color Mask 인스턴스 생성 로직 수정
        if color_mask == QRColorMasks.SOLID_FILL:
            color_mask_instance = SolidFillColorMask(
                front_color=fill_rgb,
                back_color=back_rgb
            )
        elif color_mask ==QRColorMasks.HORIZONTAL_GRADIANT:
            color_mask_instance = mask_class(
                back_color=back_rgb,
                left_color=fill_rgb,
                right_color=back_rgb
            )
        elif color_mask == QRColorMasks.VERTICAL_GRADIANT:
            color_mask_instance = mask_class(
                back_color=back_rgb,
                bottom_color=fill_rgb,
                top_color=back_rgb
            )
        else:  # RADIAL_GRADIANT, SQUARE_GRADIANT
            mask_class = RadialGradiantColorMask if color_mask == QRColorMasks.RADIAL_GRADIANT else SquareGradiantColorMask
            color_mask_instance = mask_class(
                back_color=back_rgb,
                center_color=fill_rgb,
                edge_color=back_rgb
            )
        # QR 코드 이미지 생성
        module_drawer = _get_module_drawer(style)
        eye_style = _get_eye_style(eye_style)
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask_instance,
            embedded_image=embedded_image,
            embedded_image_ratio=embedded_image_ratio if embedded_image else 0,
        )

        # 이미지를 바이트로 변환
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()

    except Exception as e:
        traceback.print_exc()
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
    URL QR Code 생성

    Args:
        url (str): QR Code에 인코딩할 URL.

    Returns:
        bytes: 생성된 QR 코드 이미지(PNG 포맷).
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
    Email QR Code 생성

    Args:
        email (str): 수신자 이메일 주소.
        subject (str, optional): 이메일 제목. 기본값은 "".
        body (str, optional): 이메일 본문. 기본값은 "".

    Returns:
        bytes: 생성된 QR 코드 이미지(PNG 포맷).
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
    text: str,  # text를 필수 매개변수로 변경
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25,
) -> bytes:
    """
    Plain Text QR Code 생성

    Args:
        text (str): QR Code에 인코딩할 텍스트.
        style (QRStyles): QR Code의 스타일.
        fill_color (str): QR Code 패턴의 색상.
        back_color (str): 배경색.
        color_mask (QRColorMasks): 그라데이션 효과를 위한 색상 마스크 유형.
        embedded_image (PIL.Image): QR Code 중심에 삽입할 이미지(선택 사항).
        embedded_image_ratio (float): 삽입된 이미지의 크기 비율(0.1-0.5).

    Returns:
        bytes: 생성된 QR 코드 이미지(PNG 포맷).
    """
    if text is None:
        raise ValueError("Text content is required")

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
    Phone Number QR Code 생성

    Args:
        phone_number: (+)1234567890 +는 필요하지 않음

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


def generate_wifi_qr(
    ssid: str,
    password: str = "",
    encryption: str = "WPA",
    hidden: bool = False,
    style: Type[QRStyles] = QRStyles.SQUARE_MODULE,
    fill_color: str = "black",
    back_color: str = "white",
    color_mask: Type[QRColorMasks] = QRColorMasks.SOLID_FILL,
    embedded_image: Image = None,
    embedded_image_ratio: float = 0.25
) -> bytes:
    """
    WiFi 설정을 위한 QR 코드 생성

    Args:
        ssid (str): WiFi SSID
        password (str, optional): WiFi 비밀번호. 기본값은 ""
        encryption (str, optional): 암호화 유형 ('WPA', 'WEP', 'none'). 기본값은 "WPA"
        hidden (bool, optional): 숨겨진 네트워크 여부. 기본값은 False
        style (QRStyles): QR 코드 스타일
        fill_color (str): QR 코드 패턴 색상
        back_color (str): 배경색
        color_mask (QRColorMasks): 색상 마스크 유형
        embedded_image (PIL.Image): 중앙에 삽입할 이미지
        embedded_image_ratio (float): 삽입 이미지 크기 비율

    Returns:
        bytes: 생성된 QR 코드 이미지(PNG 포맷)
    """
    try:
        # WiFi 문자열 생성
        wifi_string = "WIFI:"

        # 암호화 설정
        if encryption.lower() == "none":
            wifi_string += "T:nopass;"
        else:
            wifi_string += f"T:{encryption};"

        # SSID 추가
        wifi_string += f"S:{ssid};"

        # 비밀번호가 있는 경우에만 추가
        if password:
            wifi_string += f"P:{password};"

        # 숨겨진 네트워크 설정
        if hidden:
            wifi_string += "H:true;"

        # 마지막 세미콜론 추가
        wifi_string += ";"

        logger.debug(f"Generated WiFi string: {wifi_string}")  # 디버깅용 로그

        return create_qr_code(
            wifi_string,
            version=2,
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


def generate_sms_qr(
    phone_number: str,
    message: str = "",  # message를 선택적 매개변수로 변경
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
        phone_number (str): 전화번호
        message (str, optional): SMS 메시지. 기본값은 ""
        style (QRStyles): QR 코드 스타일
        fill_color (str): QR 코드 패턴 색상
        back_color (str): 배경색
        color_mask (QRColorMasks): 색상 마스크 유형
        embedded_image (PIL.Image): 중앙에 삽입할 이미지
        embedded_image_ratio (float): 삽입 이미지 크기 비율

    Returns:
        bytes: 생성된 QR 코드 이미지(PNG 포맷)
    """
    try:
        # SMS 문자열 생성
        sms = f"SMSTO:{phone_number}"
        if message:  # 메시지가 있는 경우에만 추가
            sms += f":{message}"

        logger.debug(f"Generated SMS string: {sms}")  # 디버깅용 로그

        return create_qr_code(
            sms,
            style=style,
            fill_color=fill_color,
            back_color=back_color,
            color_mask=color_mask,
            embedded_image=embedded_image,
            embedded_image_ratio=embedded_image_ratio
        )
    except Exception as e:
        logger.error(f"Error creating SMS QR Code: {e}")
        raise


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


def generate_event_qr(
    title: str,
    start: str,
    end: str,
    location: str,
    description: str,
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
        vcal += f"SUMMARY:{title}\n"
        vcal += f"DTSTART:{start}\n"
        vcal += f"DTEND:{end}\n"
        if location:
            vcal += f"LOCATION:{location}\n"
        if description:
            vcal += f"DESCRIPTION:{description}\n"
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
    name: str, reading: str, tel: str, email: str, memo: str = "", birthday: str = "", address: str = "", url: str = "", nickname: str = "",
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

def list_of_properties_of_serializer(serializer: Type[BaseQRSerializer]):
    """
    시리얼라이저에서 필수 필드만 추출
    BaseQRSerializer의 공통 필드를 제외하고 required=True인 필드만 반환
    """
    return [
        field for field, field_instance in serializer._declared_fields.items()
        if field not in BaseQRSerializer._declared_fields.keys()
        and field_instance.required
    ]
