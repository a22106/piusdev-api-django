from datetime import datetime
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpRequest
import logging

from core.supabase import supabase
from .utils import SupabaseUser  # 커스텀 사용자 클래스 임포트

logger = logging.getLogger(__name__)

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        public_paths = [
            reverse("accounts:signin"),
            reverse("accounts:signup"),
            "/",
            "/static/",
        ]

        # 세션 만료 체크
        session_data = request.session.get("supabase_session")
        if session_data: logger.debug(f"Session data: {session_data['expires_at']}")
        if session_data and session_data.get("expires_at"):
            try:
                expires_at = float(session_data["expires_at"])
                if expires_at < datetime.now().timestamp():
                    request.session.flush()
                    session_data = None
            except (ValueError, TypeError):
                request.session.flush()
                session_data = None

        # 인증 체크
        try:
            if session_data and session_data.get("access_token"):
                # 토큰 검증
                response = supabase.auth.get_user(session_data["access_token"])
                if response and response.user:
                    request.user = SupabaseUser(response.user)
                else:
                    request.session.flush()
                    request.user = AnonymousUser()
            else:
                request.user = AnonymousUser()

        except Exception as e:
            logger.error(f"Auth middleware error: {e}")
            request.session.flush()
            request.user = AnonymousUser()

        # 공개 경로는 모두 접근 허용
        if any(request.path.startswith(path) for path in public_paths):
            return self.get_response(request)

        # 인증되지 않은 사용자는 로그인 페이지로 리디렉션
        if not request.user.is_authenticated:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Unauthorized"}, status=401)
            return redirect("accounts:signin")

        return self.get_response(request)
