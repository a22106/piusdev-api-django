from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import logging

logger = logging.getLogger(__name__)


def index(request):
    qr_text = "Hello World"
    if request.method == "POST":
        logger.info(f"POST request: {request.POST}")
        qr_text = request.POST.get("url")
    return render(request, "qr/index.html", {"qr_text": qr_text})

