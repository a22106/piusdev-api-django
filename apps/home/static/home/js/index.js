$(document).ready(function() {
    const $commonOptionsForm = $('#commonOptionsForm');

    // 공통 옵션 상태 관리
    function getCommonOptions() {
        const commonOptions = {};
        $commonOptionsForm.find('input, select').each(function() {
            const $input = $(this);
            commonOptions[$input.attr('name')] = $input.val();
        });
        return commonOptions;
    }

    // 공통 옵션 상태 복원
    function restoreCommonOptions() {
        const savedOptions = localStorage.getItem('qrCommonOptions');
        if (savedOptions) {
            const options = JSON.parse(savedOptions);
            Object.entries(options).forEach(([name, value]) => {
                const $input = $commonOptionsForm.find(`[name="${name}"]`);
                if ($input.length) {
                    if ($input.attr('type') === 'file') {
                        // 파일 입력은 보안상의 이유로 복원하지 않음
                        return;
                    }
                    $input.val(value);
                }
            });
        }
    }

    // 공통 옵션 변경 감지 및 저장
    $commonOptionsForm.on('change', 'input, select', function() {
        const commonOptions = getCommonOptions();
        localStorage.setItem('qrCommonOptions', JSON.stringify(commonOptions));
    });

    // 페이지 로드 시 공통 옵션 복원
    restoreCommonOptions();

    // QR 코드 이미지 데이터를 저장할 변수
    let currentQRImageBlob = null;

    function handleQRCodeResponse(response) {
        if (response.ok) {
            return response.blob().then(blob => {
                // QR 코드 이미지 데이터 저장
                currentQRImageBlob = blob;
                
                // QR 코드 이미지 표시
                const qrImage = document.getElementById('qr-code');
                const url = URL.createObjectURL(blob);
                qrImage.src = url;
                qrImage.classList.remove('d-none');
                
                // 초기 QR 코드 이미지 숨기기
                document.getElementById('qr-code-preview').classList.add('d-none');
                
                // PNG 다운로드 버튼 설정
                const pngButton = document.getElementById('download-png');
                pngButton.classList.remove('d-none');
                pngButton.href = url;
                
                // SVG 다운로드 버튼 설정
                const svgButton = document.getElementById('download-svg');
                svgButton.classList.remove('d-none');
                
                // SVG 다운로드 버튼 클릭 이벤트
                svgButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    if (currentQRImageBlob) {
                        convertToSVG(currentQRImageBlob);
                    }
                });
            });
        } else {
            throw new Error('QR 코드 생성에 실패했습니다.');
        }
    }

    // PNG를 SVG로 변환하는 함수
    async function convertToSVG(blob) {
        try {
            // Blob을 Data URL로 변환
            const url = URL.createObjectURL(blob);
            const img = new Image();
            
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);

                // Canvas 데이터를 SVG로 변환
                const svgString = `<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                    <svg xmlns="http://www.w3.org/2000/svg" width="${img.width}" height="${img.height}">
                        <image href="${canvas.toDataURL('image/png')}" width="${img.width}" height="${img.height}"/>
                    </svg>`;
                
                // SVG 다운로드
                const svgBlob = new Blob([svgString], { type: 'image/svg+xml' });
                const svgUrl = URL.createObjectURL(svgBlob);
                const a = document.createElement('a');
                a.href = svgUrl;
                a.download = 'qr-code.svg';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                
                // 메모리 정리
                URL.revokeObjectURL(svgUrl);
            };

            img.src = url;
            
        } catch (error) {
            console.error('SVG 변환 실패:', error);
            alert('SVG 변환에 실패했습니다.');
        }
    }

    // QR 코드 폼 제출 이벤트 핸들러
    document.querySelectorAll('.qr-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 폼 데이터 수집
            const formData = new FormData(this);
            
            // 공통 옵션 폼의 데이터 추가
            const commonOptionsForm = document.getElementById('commonOptionsForm');
            const commonFormData = new FormData(commonOptionsForm);
            for (let [key, value] of commonFormData.entries()) {
                formData.append(key, value);
            }
            
            // API 요청
            fetch(this.action, {
                method: 'POST',
                body: formData
            })
            .then(handleQRCodeResponse)
            .catch(error => {
                console.error('Error:', error);
                alert(error.message);
            });
        });
    });
});
