import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.supabase import supabase
from accounts.constants import PROVIDERS
from .forms import SignUpForm, LoginForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup_form.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Supabase 회원가입 처리
        try:
            supabase.auth.sign_up(
                {
                    "email": form.cleaned_data["email"],
                    "password": form.cleaned_data["password1"],
                }
            )
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
        return response


class CustomLoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = "accounts/login_form.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            # 세션 만료 시간을 브라우저 종료시로 설정
            self.request.session.set_expiry(0)
        else:
            # 30일 동안 세션 유지
            self.request.session.set_expiry(60 * 60 * 24 * 30)

        try:
            response = supabase.auth.sign_in_with_password(
                {
                    "email": form.cleaned_data["username"],
                    "password": form.cleaned_data["password"],
                }
            )
            # 세션 저장
            self.request.session["access_token"] = response.session.access_token
            self.request.session["refresh_token"] = response.session.refresh_token
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

        return super().form_valid(form)


@method_decorator(csrf_exempt, name="dispatch")
class SignupView(View):
    @staticmethod
    def post(request):
        try:
            data = json.loads(request.body)
            email = data["email"]
            password = data["password"]
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid data"}, status=400)

        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            response_data = json.loads(response.model_dump_json())
            return JsonResponse({"data": response_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    @staticmethod
    def post(request):
        try:
            data = json.loads(request.body)
            email = data["email"]
            password = data["password"]
            remember_me = data.get("remember_me", False)

            response = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )

            # 세션 저장
            request.session["access_token"] = response.session.access_token
            request.session["refresh_token"] = response.session.refresh_token

            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30일
            else:
                request.session.set_expiry(0)  # 브라우저 종료 시 세션 삭제

            return JsonResponse(
                {
                    "success": True,
                    "data": {
                        "access_token": request.session["access_token"],
                        "refresh_token": request.session["refresh_token"],
                        "user": response.user,
                        "redirect_url": request.GET.get("next", "/"),
                    },
                }
            )

        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "error": str(e),
                },
                status=400,
            )


class LogoutView(View):
    @staticmethod
    def post(request):
        try:
            data = json.loads(request.body)
            token = data["token"]
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid data"}, status=400)

        try:
            response = supabase.auth.sign_out(token)
            response_data = json.loads(response.model_dump_json())
            return JsonResponse({"data": response_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


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


@method_decorator(csrf_exempt, name="dispatch")
class DeleteUserView(View):
    @staticmethod
    def post(request):
        try:
            # Authorization 헤더에서 토큰을 가져옴
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse(
                    {"error": "Invalid authorization header"}, status=401
                )
            print(auth_header)
            token = auth_header.split(" ")[1]

            # 사용자 삭제
            supabase.auth.admin.delete_user(token)
            return JsonResponse({"data": "User deleted"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
