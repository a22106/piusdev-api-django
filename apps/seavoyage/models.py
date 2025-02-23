from django.db import models

from apps.seavoyage.constants import DistanceUnit


class SeaRoute(models.Model):
    """해상 경로 정보를 저장하는 모델"""
    origin = models.CharField(max_length=100, verbose_name="출발지 좌표")
    destination = models.CharField(max_length=100, verbose_name="도착지 좌표")
    distance = models.FloatField(verbose_name="거리")
    units = models.CharField(max_length=10, verbose_name=f"거리 단위 ({', '.join(DistanceUnit.values())})")
    geojson = models.JSONField(verbose_name="경로 좌표 geojson")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")

    class Meta:
        verbose_name = "해상 경로"
        verbose_name_plural = "해상 경로 목록"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.origin} → {self.destination}"
