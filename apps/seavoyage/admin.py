from django.contrib import admin
from .models import SeaRoute

@admin.register(SeaRoute)
class SeaRouteAdmin(admin.ModelAdmin):
    """해상 경로 관리자 설정"""
    list_display = ('origin', 'destination', 'distance', 'created_at')
    search_fields = ('origin', 'destination')
    readonly_fields = ('created_at',)
