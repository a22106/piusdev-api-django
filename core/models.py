# core/models.py
from django.db import models

class SiteSettings(models.Model):
    title = models.CharField("Title", max_length=255, default="QR Code Generator - PiusDev")
    description = models.TextField("Description", default="Generate various types of QR codes easily and quickly.")
    keywords = models.TextField("Keywords", default="QR Code, Generator, PiusDev", max_length=255)

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
