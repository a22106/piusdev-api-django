from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

class User(AbstractUser):
    """
    사용자 모델
    기본 Django User 모델을 확장하여 필요한 필드 추가
    """
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    refresh_token = models.CharField(max_length=1000, null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # 기본적으로 새 계정은 비활성 상태로 시작
    is_active = models.BooleanField(
        '활성화 상태',
        default=False,
        help_text='이메일 인증이 필요합니다. 인증 전까지는 로그인할 수 없습니다.',
    )
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        email_username, _ = self.email.split('@')  # piushwang@piusdev.com -> piushwang, piusdev
        if self.full_name == '' or self.full_name == None:
            self.full_name = email_username
        if self.username == '' or self.username == None:
            self.username = email_username
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.username)
    
    def save(self, *args, **kwargs):
        if self.full_name == '' or self.full_name == None:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = '프로필' 

def create_user_profile(sender, instance, created, **kwargs):
    """사용자 생성 시 프로필 자동 생성"""
    if created:
        Profile.objects.create(user=instance)
        
def save_user_profile(sender, instance, **kwargs):
    """사용자 저장 시 프로필 저장"""
    instance.profile.save()

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
        
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)