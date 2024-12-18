from django.shortcuts import render
from django.views import View
import phonenumbers
from phonenumbers.data import _COUNTRY_CODE_TO_REGION_CODE
import pycountry

from core import settings
from .utils import get_country_choices
import logging

logger = logging.getLogger(__name__)

class HomeView(View):
    def get(self, request):
        context = {
            'countries': get_country_choices(),
            'debug': settings.DEBUG,
        }
        return render(request, 'home/index.html', context)
