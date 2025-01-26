import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import (
    SolidFillColorMask,
    RadialGradiantColorMask,
    SquareGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask
)
from PIL import Image
import os

def setup_test_environment():
    """테스트 환경 설정"""
    # 테스트할 색상 조합
    color_combinations = [
        {"fill": "red", "back": "white"},
        {"fill": "#0000FF", "back": "#FFFF00"},  # 파란색/노란색
        {"fill": "#00FF00", "back": "#FF00FF"},  # 녹색/마젠타
        {"fill": "#000000", "back": "#FFFFFF"},  # 검정/흰색
        {"fill": "#FF6B6B", "back": "#4ECDC4"}   # 연한 빨강/민트
    ]

    # Color Mask 종류
    color_masks = {
        "SolidFill": SolidFillColorMask,
        "RadialGradiant": RadialGradiantColorMask,
        "SquareGradiant": SquareGradiantColorMask,
        "HorizontalGradiant": HorizontalGradiantColorMask,
        "VerticalGradiant": VerticalGradiantColorMask
    }

    # 저장 디렉토리 생성
    output_dir = "qr_test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return color_combinations, color_masks, output_dir

def generate_qr_code(data, mask_type, fill_color, back_color, filename, output_dir):
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

        # Color Mask 인스턴스 생성
        if mask_type == SolidFillColorMask:
            color_mask = mask_type(front_color=fill_color, back_color=back_color)
        else:
            color_mask = mask_type(
                back_color=back_color,
                center_color=fill_color,
                edge_color=back_color
            )

        # QR 코드 이미지 생성
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=color_mask
        )

        # 이미지 저장
        output_path = os.path.join(output_dir, filename)
        img.save(output_path)
        print(f"Generated: {filename}")
        return output_path

    except Exception as e:
        print(f"Error generating {filename}: {str(e)}")
        return None

def run_color_mask_tests():
    """모든 Color Mask와 Fill Color 조합 테스트 실행"""
    # 테스트 환경 설정
    color_combinations, color_masks, output_dir = setup_test_environment()

    # 테스트 데이터
    test_data = "https://example.com"
    generated_files = []

    # 모든 조합 테스트
    for color_combo in color_combinations:
        for mask_name, mask_class in color_masks.items():
            filename = f"qr_{mask_name}_{color_combo['fill'].replace('#', '')}.png"

            output_path = generate_qr_code(
                data=test_data,
                mask_type=mask_class,
                fill_color=color_combo['fill'],
                back_color=color_combo['back'],
                filename=filename,
                output_dir=output_dir
            )

            if output_path:
                generated_files.append(output_path)

    return generated_files

def main():
    """메인 함수"""
    print("Starting QR Code Color Mask and Fill Color tests...")
    generated_files = run_color_mask_tests()

    print("\nTest Results:")
    print(f"Total QR codes generated: {len(generated_files)}")
    print("Generated files:")
    for file_path in generated_files:
        print(f"- {os.path.basename(file_path)}")

if __name__ == "__main__":
    main()