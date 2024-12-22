$(document).ready(function() {
    // Flash messages 자동 닫기
    $('.alert-dismissible').each(function() {
        const $alert = $(this);
        setTimeout(function() {
            $alert.fadeOut('slow', function() {
                $(this).remove();
            });
        }, 5000);
    });

    // Select2 초기화
    $('.select2').select2({
        theme: 'bootstrap-5'
    });

    // 네비게이션 활성화
    const currentPath = window.location.pathname;
    $('.navbar-nav .nav-link').each(function() {
        if ($(this).attr('href') === currentPath) {
            $(this).closest('.nav-item').addClass('active');
        }
    });

    // Bootstrap 툴팁 초기화
    $('[data-bs-toggle="tooltip"]').tooltip();
});