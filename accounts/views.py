import datetime
import json
import traceback
import uuid
import logging

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from core.supabase import supabase
from accounts.constants import PROVIDERS
from .forms import SignUpForm, SignInForm, DeleteUserForm

# 로거 설정
logger = logging.getLogger(__name__)


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "accounts/signup_form.html"
    success_url = reverse_lazy("qr:index")

    def form_valid(self, form):
        try:
            auth_response = supabase.auth.sign_up(
                {
                    "email": form.cleaned_data["email"],
                    "password": form.cleaned_data["password1"],
                    "options": {
                        "data": {
                            "email": form.cleaned_data["email"],
                        },
                        "email_redirect_to": f"{settings.SITE_URL}/",
                    },
                }
            )

            # Supabase 세션 저장 - 필요한 데이터만 저장
            self.request.session["supabase_session"] = {
                "access_token": auth_response.session.access_token,
                "refresh_token": auth_response.session.refresh_token,
                "expires_at": auth_response.session.expires_at,
            }

            # Django 사용자 생성 또는 가져오기
            User = get_user_model()
            user, created = User.objects.get_or_create(
                email=form.cleaned_data["email"],
                defaults={
                    "username": form.cleaned_data["email"],  # 이메일을 username으로 사용
                }
            )

            # Django 로그인 처리
            login(self.request, user)

            messages.success(self.request, "Successfully signed up. Please check your email.")
            return super().form_valid(form)
        except Exception as e:
            # 에러 메시지를 전달
            logger.error(f"Sign up error: {str(e)}")
            messages.error(self.request, f"Sign up error: {str(e)}")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["debug"] = settings.DEBUG
        return context

class SignInView(View):
    form_class = SignInForm
    template_name = "accounts/signin_form.html"

    def get_success_url(self):
        return reverse_lazy("qr:index")

    def get(self, request: HttpRequest):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                # Supabase 로그인
                response = supabase.auth.sign_in_with_password({
                    "email": form.cleaned_data["email"],
                    "password": form.cleaned_data["password"],
                })

                # Supabase 세션 저장
                request.session["supabase_session"] = {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "expires_at": response.session.expires_at,
                }

                # Django 사용자 생성 또는 가져오기
                User = get_user_model()
                user, created = User.objects.get_or_create(
                    email=form.cleaned_data["email"],
                    defaults={
                        "username": form.cleaned_data["email"],  # 이메일을 username으로 사용
                    }
                )

                # Django 로그인 처리
                login(request, user)

                if not form.cleaned_data.get("remember_me"):
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(60 * 60 * 24 * 30)  # 30일

                messages.success(request, "Successfully logged in.")
                return redirect(self.get_success_url())

            except Exception as e:
                logger.error(f"Login error: {e}")
                messages.error(request, f"Login error: {str(e)}")
                return render(request, self.template_name, {"form": form})

        return render(request, self.template_name, {"form": form})


class LogOutView(View):
    def get(self, request):
        try:
            # Supabase 로그아웃
            supabase.auth.sign_out()

            # Django 로그아웃
            logout(request)

            # Django 세션에서 Supabase 관련 데이터 삭제
            request.session.pop("supabase_session", None)
            request.session.pop("user", None)

            messages.success(request, "Successfully logged out.")
            return redirect("/")
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            messages.error(request, "Logout error.")
            return redirect("/")


# provider login
@method_decorator(csrf_exempt, name="dispatch")
class ProviderLoginView(View):
    @staticmethod
    def post(request):
        try:
            data = json.loads(request.body)
            provider = data["provider"]
            token = data["token"]
            if provider not in PROVIDERS:
                return JsonResponse({"error": "Invalid provider"}, status=400)
            response = supabase.auth.sign_in_with_id_token(
                {"provider": provider, "token": token}
            )
            response_data = json.loads(response.model_dump_json())
            return JsonResponse({"data": response_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class DeleteUserView(View):
    def post(self, request):
        if not settings.DEBUG:
            return JsonResponse({"error": "Not allowed"}, status=403)

        form = DeleteUserForm(request.POST)
        if form.is_valid():
            try:
                user_uuid = form.cleaned_data["user_uuid"]
                supabase.auth.admin.delete_user(str(user_uuid))
                return redirect("accounts:signup")
            except Exception as e:
                return render(
                    request,
                    "accounts/signup_form.html",
                    {"form": form, "error": str(e)},
                )

        return redirect("accounts:signup")


class VerifyEmailView(View):
    def get(self, request, token):
        # Removed Django's email verification logic
        messages.success(request, "Email verification successful.")
        return redirect("/")
