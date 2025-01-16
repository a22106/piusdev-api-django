import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

class User(AbstractUser):
    """
    사용자 모델
    기본 Django User 모델을 확장하여 필요한 필드 추가
    """
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)

    # 기본적으로 새 계정은 비활성 상태로 시작
    is_active = models.BooleanField(
        '활성화 상태',
        default=False,
        help_text='이메일 인증이 필요합니다. 인증 전까지는 로그인할 수 없습니다.',
    )

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
        
@receiver(pre_save, sender=User)
def set_superuser_for_specific_email(sender, instance, **kwargs):
    """
    특정 이메일(bk22106@gmail.com)로 가입하는 경우
    자동으로 superuser 권한을 부여하고 활성화합니다.
    """
    if instance.email == 'bk22106@gmail.com':
        instance.is_superuser = True
        instance.is_staff = True
        instance.is_active = True