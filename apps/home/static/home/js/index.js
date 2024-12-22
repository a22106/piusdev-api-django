$(document).ready(function() {
    // QR 코드 관련 요소 선택
    const $qrCodePreview = $('#qr-code-preview');
    const $qrCode = $('#qr-code');
    const $downloadPng = $('#download-png');
    const $downloadSvg = $('#download-svg');

    // Select2 초기화
    $('.country-code-select').select2({
        theme: 'bootstrap-5',
        placeholder: 'Select a country',
        allowClear: true,
        width: 'resolve'
    });

    // QR 코드 생성 폼 제출 처리
    $('.qr-form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var formData = new FormData(this);

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
                // QR 코드 이미지를 Base64로 변환하여 표시
                var imageUrl = URL.createObjectURL(new Blob([response], {type: 'image/png'}));
                $('#qr-preview').html('<img src="' + imageUrl + '" class="img-fluid" alt="QR Code">');

                // 다운로드 버튼 표시
                $('#download-png, #download-svg').removeClass('d-none');
            },
            error: function(xhr, status, error) {
                var errorMessage = xhr.responseJSON ? xhr.responseJSON.detail : 'An error occurred';
                alert('Error: ' + errorMessage);

                // 에러 발생 시 다운로드 버튼 숨김
                $('#download-png, #download-svg').addClass('d-none');
            }
        });
    });

    // PNG 다운로드 처리
    $('#download-png').click(function() {
        var qrImage = $('#qr-preview img');
        if (qrImage.length) {
            var link = document.createElement('a');
            link.href = qrImage.attr('src');
            link.download = `qr-code-${Date.now()}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    });

    // SVG 다운로드 처리
    $('#download-svg').click(function() {
        var qrImage = $('#qr-preview img');
        if (qrImage.length) {
            // PNG를 SVG로 변환
            var img = new Image();
            img.onload = function() {
                var canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                var ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);

                // SVG 생성
                var svg = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="${img.width}" height="${img.height}">
                        <image href="${canvas.toDataURL('image/png')}" width="${img.width}" height="${img.height}"/>
                    </svg>
                `;

                // SVG 다운로드
                var blob = new Blob([svg], { type: 'image/svg+xml' });
                var url = URL.createObjectURL(blob);
                var link = document.createElement('a');
                link.href = url;
                link.download = `qr-code-${Date.now()}.svg`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
            };
            img.src = qrImage.attr('src');
        }
    });
});
