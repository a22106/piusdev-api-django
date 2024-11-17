from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

from accounts.tests.utils import TEST_USER_EMAIL, TEST_USER_PASSWORD, create_test_user, delete_test_user

logger = logging.getLogger(__name__)

class TestSignUp(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_id = create_test_user()

    @classmethod
    def tearDownClass(cls):
        if cls.user_id:
            delete_test_user(cls.user_id)
        super().tearDownClass()

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_signup(self):
        self.driver.get(f"{self.live_server_url}/auth/signup/")

        # 폼 필드 찾기
        email_field = self.driver.find_element(By.NAME, "email")
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