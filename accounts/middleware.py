from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse
import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        public_paths = [
            reverse("accounts:signin"),
            reverse("accounts:signup"),
            "/",
            "/static/",
        ]

        if any(request.path.startswith(path) for path in public_paths):
            return

        if not request.user.is_authenticated:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Unauthorized"}, status=401)
            return redirect("accounts:signin")
