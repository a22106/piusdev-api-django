from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import (
    URLQRForm, TextQRForm, EmailQRForm, PhoneQRForm,
    SMSQRForm, WhatsAppQRForm, WiFiQRForm, VCardQRForm
)
import logging

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 각 탭에 대한 폼 인스턴스 생성
        context.update({
            'url_form': URLQRForm(),
            'text_form': TextQRForm(),
            'email_form': EmailQRForm(),
            'phone_form': PhoneQRForm(),
            'sms_form': SMSQRForm(),
            'whatsapp_form': WhatsAppQRForm(),
            'wifi_form': WiFiQRForm(),
            'vcard_form': VCardQRForm(),
        })

        return context
