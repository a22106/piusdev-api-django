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

    // QR 코드 생성 폼 제출 처리
    $('.qr-form').on('submit', function(e) {
        e.preventDefault();
        const form = $(this);
        const formData = new FormData(this);

        // 공통 옵션 추가
        const commonOptions = getCommonOptions();
        Object.entries(commonOptions).forEach(([name, value]) => {
            // 파일 입력은 별도 처리
            if (name === 'embedded_image') {
                const fileInput = $commonOptionsForm.find('input[type="file"]')[0];
                if (fileInput.files.length > 0) {
                    formData.append(name, fileInput.files[0]);
                }
            } else {
                formData.append(name, value);
            }
        });

        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            xhrFields: {
                responseType: 'blob'
            },
            success: function(response) {
                var imageUrl = URL.createObjectURL(new Blob([response], {type: 'image/png'}));
                $('#qr-preview').html('<img src="' + imageUrl + '" class="img-fluid" alt="QR Code">');

                // 다운로드 버튼 표시
                $('#download-png, #download-svg').removeClass('d-none');
            },
            error: function(xhr, status, error) {

                // 에러 발생 시 다운로드 버튼 숨김
                var errorMessage = xhr.responseJSON ? xhr.responseJSON.detail : 'An error occurred';
                alert('Error: ' + errorMessage);
                $('#download-png, #download-svg').addClass('d-none');
            }
        });
    });

    // 기존의 다운로드 버튼 처리 코드...
});
