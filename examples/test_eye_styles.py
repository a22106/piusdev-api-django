import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from PIL import Image
import os

def setup_test_environment():
    """테스트 환경 설정"""
    # QR 코드 eye 스타일 설정
    eye_styles = {
        "Square": {
            "eye_drawer": None,  # 기본 사각형 스타일
        },
        "Circle": {
            "eye_drawer": CircleModuleDrawer(),  # 원형 스타일
        },
        "RoundedSquare": {
            "eye_drawer": RoundedModuleDrawer(),  # 둥근 모서리 스타일
        }
    }

    # 저장 디렉토리 생성
    output_dir = "qr_eye_test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return eye_styles, output_dir

def generate_qr_code_with_eye_style(data, eye_style, filename, output_dir):
    """QR 코드 생성 함수"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # 기본 색상 설정
        color_mask = SolidFillColorMask(
            front_color=(0, 0, 0),
            back_color=(255, 255, 255)
        )

        # QR 코드 이미지 생성
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=eye_style["eye_drawer"],
            color_mask=color_mask,
            eye_drawer=eye_style["eye_drawer"]  # eye 스타일 적용
        )

        # 이미지 저장
        output_path = os.path.join(output_dir, filename)
        img.save(output_path)
        print(f"Generated: {filename}")
        return output_path

    except Exception as e:
        print(f"Error generating {filename}: {str(e)}")
        return None

def run_eye_style_tests():
    """모든 eye 스타일 테스트 실행"""
    # 테스트 환경 설정
    eye_styles, output_dir = setup_test_environment()

    # 테스트 데이터
    test_data = "https://example.com"
    generated_files = []

    # 각 eye 스타일 테스트
    for style_name, style_config in eye_styles.items():
        filename = f"qr_eye_style_{style_name}.png"

        output_path = generate_qr_code_with_eye_style(
            data=test_data,
            eye_style=style_config,
            filename=filename,
            output_dir=output_dir
        )

        if output_path:
            generated_files.append(output_path)

    return generated_files

def main():
    """메인 함수"""
    print("Starting QR Code Eye Style tests...")
    generated_files = run_eye_style_tests()

    print("\nTest Results:")
    print(f"Total QR codes generated: {len(generated_files)}")
    print("Generated files:")
    for file_path in generated_files:
        print(f"- {os.path.basename(file_path)}")

if __name__ == "__main__":
    main()