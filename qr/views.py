from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
import qrcode
from io import BytesIO

from rest_framework.views import APIView

from qr.utils.qr_utils import generate_qr_image

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "qr/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "QR Code Generator"
        context["description"] = "A simple QR Code generator"
        context["keywords"] = "QR Code, Generator"
        context["qr_text"] = "Hello World"
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        qr_text = request.POST.get("url")
        logger.info(f"QR Text: {qr_text}")
        context["qr_text"] = qr_text
        return self.render_to_response(context)


class QrImageView(View):

    @method_decorator(require_http_methods(["POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        qr_text = request.POST.get("text", "Hello World")
        return generate_qr_image(qr_text)  # Utilized the utility function


class QrApiView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["text"],
            properties={
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="QR Text")
            },
        ),
        responses={200: openapi.Response("QR Code Image (PNG)")},
    )
    def post(self, request):
        qr_text = request.data.get("text", "Hello World")
        return generate_qr_image(qr_text)  # Utilized the utility function


# swagger endpoint response {"detail": "Hello World"}
class HelloWorldView(APIView):
    @swagger_auto_schema(
        operation_description="This is a test view",
        responses={200: openapi.Response("Hello World")},
    )
    def get(self, request):
        return HttpResponse("Hello World")


class HelloDjangoView(APIView):
    @swagger_auto_schema(
        operation_description="This is a test view",
        responses={200: openapi.Response("Hello Django")},
    )
    def post(self, request):
        return HttpResponse("Hello Django")
