import json
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.supabase import supabase
from qr_auth.constants import PROVIDERS


class LoginPageView(View):
    def get(self, request):
        return render(request, "registration/login.html")


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
                
            return JsonResponse({
                "success": True,
                "data": {
                    "access_token": request.session["access_token"],
                    "refresh_token": request.session["refresh_token"],
                    "user": response.user,
                    "redirect_url": request.GET.get("next", "/"),
                },
            })
            
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e),
            }, status=400)


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
