$(document).ready(function() {
    // QR 코드 관련 요소 선택
    const $qrCodePreview = $('#qr-code-preview');
    const $qrCode = $('#qr-code');
    const $downloadPng = $('#download-png');
    const $downloadSvg = $('#download-svg');

    // Select2 초기화
    $('.country-code-select').select2({
        theme: 'bootstrap-5',
        placeholder: 'Select Country Code',
        allowClear: true,
        width: 'resolve'
    });

    // CSRF 토큰 설정
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // 폼 제출 이벤트 처리
    $('.qr-form').on('submit', function(e) {
        e.preventDefault();

        const $form = $(this);
        const formData = new FormData(this);

        // 전화번호 처리 (있는 경우)
        const $countryCode = $form.find('select[name="country_code"]');
        const $phoneNumber = $form.find('input[name="phone_number"]');

        if ($countryCode.length && $phoneNumber.length) {
            const fullNumber = ($countryCode.val() + $phoneNumber.val()).replace(/[+\s-]/g, '');
            formData.set('phone_number', fullNumber);
        }

        $.ajax({
            url: $form.attr('action'),
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // QR 코드 이미지 업데이트
                $qrCodePreview.addClass('d-none');
                $qrCode.attr('src', 'data:image/png;base64,' + response.image)
                       .removeClass('d-none');

                // 다운로드 버튼 활성화
                $downloadPng.removeClass('d-none');
                $downloadSvg.removeClass('d-none');
            },
            error: function(xhr, status, error) {
                alert('Error generating QR code: ' + error);
            }
        });
    });

    // PNG 다운로드 처리
    $downloadPng.click(function() {
        if ($qrCode.attr('src')) {
            const link = document.createElement('a');
            link.href = $qrCode.attr('src');
            link.download = 'qr-code.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    });

    // SVG 다운로드 처리
    $downloadSvg.click(function() {
        // SVG 다운로드 로직 구현
    });
});
