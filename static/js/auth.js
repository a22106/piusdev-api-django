async function handleLogin(event) {
    event.preventDefault();
    
    const formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        remember_me: document.getElementById('remember-me').checked
    };

    try {
        const response = await fetch('/auth/v1/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            // 토큰 저장
            localStorage.setItem('access_token', data.data.access_token);
            sessionStorage.setItem('refresh_token', data.data.refresh_token);
            
            // 사용자 정보 저장
            localStorage.setItem('user', JSON.stringify(data.data.user));

            // 리다이렉트
            window.location.href = data.data.redirect_url;
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Login failed. Please try again.');
    }
}

// 토큰 갱신 함수
async function refreshToken() {
    const refresh_token = sessionStorage.getItem('refresh_token');
    if (!refresh_token) return null;

    try {
        const response = await fetch('/auth/v1/refresh-token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh_token })
        });

        const data = await response.json();
        if (data.success) {
            localStorage.setItem('access_token', data.data.access_token);
            return data.data.access_token;
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
        return null;
    }
} 