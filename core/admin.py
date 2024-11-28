# core/admin.py
from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # 인스턴스가 하나만 존재하도록 추가 권한 제한
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # 인스턴스가 하나만 존재하도록 삭제 권한 제한
        return False

