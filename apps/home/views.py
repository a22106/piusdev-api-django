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

        # 국가 코드 리스트
        countries = []
        for country in sorted(pycountry.countries, key=lambda x: x.name):
            try:
                country_code = phonenumbers.country_code_for_region(country.alpha_2)
                countries.append(
                    {
                        "name": country.name,
                        "dial_code": f"+{country_code}",
                    }
                )
            except:
                logger.error(f"Error getting country code for {country.name}")
                raise
        context["countries"] = countries
        context['debug'] = settings.DEBUG
        return context
