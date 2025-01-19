import pytest
from playwright.sync_api import sync_playwright, Page, expect
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class PlaywrightTest(StaticLiveServerTestCase):
    def test_homepage(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url)
            assert "PiusDev" in page.title()
            browser.close()

class QRCodeGenerationTest(StaticLiveServerTestCase):
    """QR 코드 생성 기능 E2E 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)  # 디버깅을 위해 headless=False로 설정
        self.page = self.browser.new_page()
        self.page.set_default_timeout(5000)  # 타임아웃 시간
        self.page.goto(f"{self.live_server_url}")

    def tearDown(self):
        """테스트 종료 및 리소스 정리"""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def wait_for_qr_code(self):
        """QR 코드 생성 대기"""
        self.page.wait_for_selector("#qr-code-preview", state="visible")
        self.page.wait_for_selector("#download-png", state="visible")

    def submit_form_and_verify(self, tab_id):
        """폼 제출 및 결과 확인"""
        # 현재 활성화된 탭의 Generate QR Code 버튼 찾기
        submit_button = self.page.locator(f"#{tab_id} button[type='submit']")
        submit_button.wait_for(state="visible")
        submit_button.click()
        
        # QR 코드 생성 확인
        self.wait_for_qr_code()

    def test_url_qr_generation(self):
        """URL QR 코드 생성 테스트"""
        # URL 탭이 기본적으로 활성화되어 있는지 확인
        active_tab = self.page.locator(".nav-link.active")
        expect(active_tab).to_have_text("URL")

        # URL 입력
        url_input = self.page.locator("input[name='url']")
        url_input.wait_for(state="visible")
        url_input.fill("https://example.com")

        self.submit_form_and_verify("url")

    def test_text_qr_generation(self):
        """텍스트 QR 코드 생성 테스트"""
        # Text 탭으로 이동
        self.page.click("a[href='#text']")
        
        # 텍스트 입력
        text_input = self.page.locator("#text textarea[name='text']")
        text_input.wait_for(state="visible")
        text_input.fill("Hello, QR Code!")

        self.submit_form_and_verify("text")

    def test_email_qr_generation(self):
        """이메일 QR 코드 생성 테스트"""
        # Email 탭으로 이동
        self.page.click("a[href='#email']")
        
        # 이메일 정보 입력
        self.page.locator("#email input[name='email']").fill("test@example.com")
        self.page.locator("#email input[name='subject']").fill("Test Subject")
        self.page.locator("#email textarea[name='body']").fill("Test Email Body")

        self.submit_form_and_verify("email")

    def test_phone_qr_generation(self):
        """전화번호 QR 코드 생성 테스트"""
        # Phone 탭으로 이동
        self.page.click("a[href='#phone']")
        
        # 전화번호 입력
        phone_input = self.page.locator("#phone input[name='phone_number']")
        phone_input.wait_for(state="visible")
        phone_input.fill("+821012345678")

        self.submit_form_and_verify("phone")

    def test_sms_qr_generation(self):
        """SMS QR 코드 생성 테스트"""
        # SMS 탭으로 이동
        self.page.click("a[href='#sms']")
        
        # SMS 정보 입력
        self.page.locator("#sms input[name='phone_number']").fill("+821012345678")
        self.page.locator("#sms textarea[name='message']").fill("Test SMS message")

        self.submit_form_and_verify("sms")

    def test_whatsapp_qr_generation(self):
        """WhatsApp QR 코드 생성 테스트"""
        # WhatsApp 탭으로 이동
        self.page.click("a[href='#whatsapp']")
        
        # WhatsApp 정보 입력
        self.page.locator("#whatsapp input[name='phone_number']").fill("+821012345678")
        self.page.locator("#whatsapp textarea[name='message']").fill("Test WhatsApp message")

        self.submit_form_and_verify("whatsapp")

    def test_wifi_qr_generation(self):
        """WiFi QR 코드 생성 테스트"""
        # WiFi 탭으로 이동
        self.page.click("a[href='#wifi']")
        
        # WiFi 정보 입력
        self.page.locator("#wifi input[name='ssid']").fill("TestWiFi")
        self.page.locator("#wifi input[name='password']").fill("testpassword123")
        self.page.locator("#wifi select[name='encryption']").select_option("WPA")

        self.submit_form_and_verify("wifi")

    def test_vcard_qr_generation(self):
        """VCard QR 코드 생성 테스트"""
        # VCard 탭으로 이동
        self.page.click("a[href='#vcard']")
        
        # VCard 정보 입력
        form = self.page.locator("#vcard")
        form.locator("input[name='first_name']").fill("John")
        form.locator("input[name='last_name']").fill("Doe")
        form.locator("input[name='vcard_email']").fill("john.doe@example.com")
        form.locator("input[name='vcard_mobile']").fill("+821012345678")
        form.locator("input[name='organization']").fill("Test Company")
        form.locator("input[name='job_title']").fill("Software Engineer")
        form.locator("input[name='vcard_url']").fill("https://example.com")

        self.submit_form_and_verify("vcard")

    def test_qr_common_options(self):
        """QR 코드 공통 옵션 테스트"""
        # 공통 옵션 패널 열기
        self.page.click("button[data-bs-target='#commonQrOptions']")
        
        # 옵션 패널이 열릴 때까지 대기
        self.page.wait_for_selector("#commonQrOptions.show")
        
        # 스타일 변경
        self.page.locator("select[name='style']").select_option("ROUNDED_MODULE")
        
        # 색상 마스크 변경
        self.page.locator("select[name='color_mask']").select_option("RADIAL_GRADIANT")
        
        # 색상 변경
        self.page.evaluate("""() => {
            document.querySelector("input[name='fill_color']").value = '#FF0000';
            document.querySelector("input[name='back_color']").value = '#FFFFFF';
        }""")
        
        # 임베디드 이미지 비율 변경
        self.page.locator("input[name='embedded_image_ratio']").fill("0.3")
        
        # URL QR 코드 생성 테스트
        self.page.locator("#url input[name='url']").fill("https://example.com")
        
        self.submit_form_and_verify("url")
