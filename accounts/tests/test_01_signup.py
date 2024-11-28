from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

from accounts.tests.utils import TEST_USER_EMAIL, TEST_USER_PASSWORD

logger = logging.getLogger(__name__)

class TestSignUp(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 회원가입 테스트 시 이미 테스트 사용자가 생성되었으므로 별도 생성을 생략

    @classmethod
    def tearDownClass(cls):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=TEST_USER_EMAIL)
            user.delete()
        except user_model.DoesNotExist:
            pass
        super().tearDownClass()

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_signup(self):
        self.driver.get(f"{self.live_server_url}/auth/signup/")

        # Wait up to 10 seconds for the email field to be present
        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )

        # 폼 필드 찾기
        password1_field = self.driver.find_element(By.NAME, "password1")
        password2_field = self.driver.find_element(By.NAME, "password2")
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        # 가입 정보 입력
        email_field.send_keys(TEST_USER_EMAIL)
        password1_field.send_keys(TEST_USER_PASSWORD)
        password2_field.send_keys(TEST_USER_PASSWORD)

        # 폼 제출
        submit_button.click()

        # 가입 성공 확인
        time.sleep(2)  # 페이지 로딩 대기
        success_message = self.driver.find_elements(By.CLASS_NAME, "alert-success")
        assert len(success_message) > 0, "가입 성공 메시지를 찾을 수 없습니다."