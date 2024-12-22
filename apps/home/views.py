from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
import phonenumbers
from phonenumbers.data import _COUNTRY_CODE_TO_REGION_CODE
import pycountry

from core import settings
from .utils import get_country_choices
import logging

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)



        context["countries"] = get_country_choices()
        context['debug'] = settings.DEBUG
        return context
