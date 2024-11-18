from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

from accounts.tests.utils import TEST_USER_EMAIL, TEST_USER_PASSWORD
from django.conf import settings

logger = logging.getLogger(__name__)

class TestSignIn(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username=TEST_USER_EMAIL,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_signin(self):
        self.driver.get(f"{self.live_server_url}/auth/signin/")

        # 로그인 폼 필드 찾기
        email_field = self.driver.find_element(By.NAME, "email")
        password_field = self.driver.find_element(By.NAME, "password")
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        # 로그인 정보 입력
        email_field.send_keys(TEST_USER_EMAIL)
        password_field.send_keys(TEST_USER_PASSWORD)

        # 폼 제출
        submit_button.click()

        # 로그인 성공 확인 (예: 성공 메시지 또는 리디렉션 확인)
        time.sleep(2)  # 페이지 로딩 대기
        success_message = self.driver.find_elements(By.CLASS_NAME, "alert-success")
        assert len(success_message) > 0, "로그인 성공 메시지를 찾을 수 없습니다."

        # 추가적인 검증 (예: 사용자 계정 페이지로 리디렉션)
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        expected_url = self.live_server_url + "/"
        assert current_url == expected_url, f"예상된 리디렉션 URL이 아닙니다: 예상: {expected_url}, 실제: {current_url}"