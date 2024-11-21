from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        # is_active 상태와 관계없이 로그인 허용
        return True