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
    def post(self, request, *args, **kwargs):
        qr_text = request.POST.get("text", "Hello World")
        logger.info(f"QR Text: {qr_text}")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, "PNG")
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type="image/png")
