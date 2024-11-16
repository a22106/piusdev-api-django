import datetime
import json
import traceback

from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages

from core.supabase import supabase
from accounts.constants import PROVIDERS
from .forms import SignUpForm, SignInForm, DeleteUserForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup_form.html"
    success_url = "/"

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
                        "email_redirect_to": f"{settings.SITE_URL}/accounts/verify-email"  # 이메일 인증 후 리다이렉트될 URL
                    }
                }
            )
            # 세션 정보 저장
            self.request.session["access_token"] = auth_response.session.access_token
            self.request.session["refresh_token"] = auth_response.session.refresh_token
            self.request.session["expires_at"] = auth_response.session.expires_at

            # 사용자 정보 저장
            self.request.session["user"] = {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "role": auth_response.user.role,
                "created_at": int(auth_response.user.created_at.timestamp()),
            }

            # Django 로그인 처리

            user_model = get_user_model()
            user = user_model.objects.create_user(
                username=auth_response.user.email,
                email=auth_response.user.email,
                password=form.cleaned_data["password1"],
                is_active=False,
            )

            # # Django 로그인 처리
            # login(self.request, user)

            # 이메일 인증 토큰 생성
            signer = TimestampSigner()
            token = signer.sign(user.id)

            # 이메일 인증 전송
            verification_url = f"{settings.SITE_URL}/accounts/verify-email/{token}"
            email_context = {
                "verification_url": verification_url,
                "user_email": user.email,
            }
            email_html = render_to_string("accounts/verify_email_template.html", email_context)
            email_text = render_to_string("accounts/verify_email_template.txt", email_context)

            send_mail(
                subject="Verify your email",
                message=email_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=email_html,
                fail_silently=False,
            )


            messages.success(self.request, "Please check your email for verification.")
            return redirect("/")

        except Exception as e:
            form.add_error(None, str(e))
            print(traceback.format_exc())
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["debug"] = settings.DEBUG
        return context


class SignInView(DjangoLoginView):
    form_class = SignInForm
    template_name = "accounts/signin_form.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        # 로그인 성공 후 리다이렉트할 URL
        return reverse_lazy("qr:index")

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
                    "email": form.cleaned_data["email"],
                    "password": form.cleaned_data["password"],
                }
            )
            # 세션 저장
            self.request.session["access_token"] = response.session.access_token
            self.request.session["refresh_token"] = response.session.refresh_token
            self.request.session["expires_at"] = response.session.expires_at

            user_model = get_user_model()
            user = user_model.objects.get(email=response.user.email)
            login(self.request, user)

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


class SignOutView(View):
    def get(self, request):
        try:
            # Supabase 로그아웃
            supabase.auth.sign_out()

            # Django 세션에서 Supabase 관련 데이터 삭제
            request.session.pop("access_token", None)
            request.session.pop("refresh_token", None)
            request.session.pop("expires_at", None)
            request.session.pop("user", None)

            # Django 로그아웃
            from django.contrib.auth import logout

            logout(request)

            return redirect("/")
        except Exception as e:
            print(f"Logout error: {str(e)}")
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
        try:
            signer = TimestampSigner()
            email = signer.unsign(token, max_age=60 * 60 * 24) # 24시간 유효

            user_model = get_user_model()
            user = user_model.objects.get(email=email)

            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, "Your email has been verified.")
            else:
                messages.info(request, "Your email has already been verified.")

            return redirect("/")
        except SignatureExpired:
            messages.error(request, "The verification link has expired.")
            return redirect("/")
        except (BadSignature, user_model.DoesNotExist):
            messages.error(request, "The verification link is invalid.")
            return redirect("/")
