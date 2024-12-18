from django.conf import settings
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

TEST_USER_EMAIL = "test_user@example.com"
TEST_USER_PASSWORD = "TestPassword123!"

def create_test_user():
    try:
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username=TEST_USER_EMAIL,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD
        )
        logger.info(f"테스트 사용자 생성: {TEST_USER_EMAIL}")
        return user.id
    except Exception as e:
        logger.error(f"테스트 사용자 생성 실패: {e}")
        return None

def delete_test_user(user_id):
    try:
        user_model = get_user_model()
        user = user_model.objects.get(id=user_id)
        user.delete()
        logger.info(f"테스트 사용자 삭제: {TEST_USER_EMAIL}")
    except Exception as e:
        logger.error(f"테스트 사용자 삭제 실패: {e}")