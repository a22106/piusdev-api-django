from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect

from core.supabase import supabase


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 인증이 필요없는 경로들
        public_paths = [
            reverse("accounts:login"),
            reverse("accounts:signup"),
            "/static/",
        ]

        # 현재 경로가 public_paths에 포함되어 있으면 인증 체크 스킵
        if any(request.path.startswith(path) for path in public_paths):
            return self.get_response(request)

        # 세션에서 토큰 확인
        access_token = request.session.get("access_token")

        if not access_token:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Unauthorized"}, status=401)
            return redirect("accounts:login")

        # 토큰 유효성 검증
        try:
            # Supabase 토큰 검증
            user = supabase.auth.get_user(access_token)
            request.user = user
        except Exception:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Invalid token"}, status=401)
            return redirect("accounts:login")

        return self.get_response(request)
