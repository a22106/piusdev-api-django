import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    HorizontalBarsDrawer,
    VerticalBarsDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image
import os

def setup_test_environment():
    """테스트 환경 설정"""
    # 테스트할 스타일 설정
    style_drawers = {
        "Square": SquareModuleDrawer(),
        "GappedSquare": GappedSquareModuleDrawer(),
        "Circle": CircleModuleDrawer(),
        "Rounded": RoundedModuleDrawer(),
        "HorizontalBars": HorizontalBarsDrawer(),
        "VerticalBars": VerticalBarsDrawer()
    }

    # 테스트할 크기 조합
    size_combinations = [
        {"box_size": 10, "border": 4},  # 기본 크기
        {"box_size": 15, "border": 6},  # 큰 크기
        {"box_size": 5, "border": 2},   # 작은 크기
    ]

    # 저장 디렉토리 생성
    output_dir = "qr_style_test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return style_drawers, size_combinations, output_dir

def generate_qr_code(data, style_drawer, box_size, border, filename, output_dir):
    """QR 코드 생성 함수"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # 기본 색상 마스크 설정
        color_mask = SolidFillColorMask(
            front_color=(0, 0, 0),
            back_color=(255, 255, 255)
        )

        # QR 코드 이미지 생성
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=style_drawer,
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

def run_style_tests():
    """모든 스타일과 크기 조합 테스트 실행"""
    # 테스트 환경 설정
    style_drawers, size_combinations, output_dir = setup_test_environment()

    # 테스트 데이터
    test_data = "https://example.com"
    generated_files = []

    # 모든 조합 테스트
    for style_name, drawer in style_drawers.items():
        for size in size_combinations:
            filename = f"qr_style_{style_name}_box{size['box_size']}_border{size['border']}.png"

            output_path = generate_qr_code(
                data=test_data,
                style_drawer=drawer,
                box_size=size['box_size'],
                border=size['border'],
                filename=filename,
                output_dir=output_dir
            )

            if output_path:
                generated_files.append(output_path)

    return generated_files

def test_with_embedded_image():
    """임베디드 이미지가 있는 스타일 테스트"""
    style_drawers, _, output_dir = setup_test_environment()
    generated_files = []
    test_data = "https://example.com"

    # 테스트용 임베디드 이미지 생성
    embedded_img = Image.new('RGB', (50, 50), color='red')
    embedded_img_path = os.path.join(output_dir, 'test_embedded.png')
    embedded_img.save(embedded_img_path)

    for style_name, drawer in style_drawers.items():
        filename = f"qr_style_{style_name}_with_embedded.png"

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(test_data)
            qr.make(fit=True)

            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=drawer,
                embeded_image=embedded_img,
                embeded_image_ratio=0.2
            )

            output_path = os.path.join(output_dir, filename)
            img.save(output_path)
            print(f"Generated: {filename}")
            generated_files.append(output_path)

        except Exception as e:
            print(f"Error generating {filename}: {str(e)}")

    return generated_files

def main():
    """메인 함수"""
    print("Starting QR Code Style tests...")

    # 기본 스타일 테스트
    print("\nRunning basic style tests...")
    basic_files = run_style_tests()

    # 임베디드 이미지 테스트
    print("\nRunning embedded image tests...")
    embedded_files = test_with_embedded_image()

    # 결과 출력
    print("\nTest Results:")
    print(f"Total QR codes generated: {len(basic_files) + len(embedded_files)}")
    print("\nBasic style files:")
    for file_path in basic_files:
        print(f"- {os.path.basename(file_path)}")

    print("\nEmbedded image style files:")
    for file_path in embedded_files:
        print(f"- {os.path.basename(file_path)}")

if __name__ == "__main__":
    main()