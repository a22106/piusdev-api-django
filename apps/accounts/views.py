import logging
import random
import string

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from apps.accounts import serializer
from apps.accounts.models import User
from .forms import SignUpForm, SignInForm, DeleteUserForm
from .tokens import email_verification_token
logger = logging.getLogger(__name__)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializer.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = serializer.RegisterSerializer

class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "accounts/signup_form.html"
    success_url = reverse_lazy("home:index")

    def form_valid(self, form: SignUpForm):
        try:
            user_model = get_user_model()
            user = user_model.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                is_active=False,
            )

            try:
                current_site = get_current_site(self.request)
                subject = "Verify your email"
                message = render_to_string(
                    "accounts/email_verification.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": email_verification_token.make_token(user),
                    },
                )
                user.email_user(subject, message)
                messages.success(self.request, "Successfully signed up. Please check your email.")
            except Exception as email_error:
                logger.error(f"Email sending error: {str(email_error)}")
                messages.warning(
                    self.request,
                    "Account created successfully, but verification email could not be sent. "
                    "Please contact support."
                )

            login(self.request, user, backend='accounts.backends.CustomAuthBackend')
            return super().form_valid(form)

        except Exception as e:
            logger.error(f"Signup error: {str(e)}")
            messages.error(self.request, "An error occurred during signup. Please try again.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["debug"] = settings.DEBUG
        return context


class SignInView(FormView):
    form_class = SignInForm
    template_name = "accounts/signin_form.html"
    success_url = reverse_lazy("home:index")

    def form_valid(self, form: SignInForm):
        username = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        remember_me = form.cleaned_data.get("remember_me")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            if not remember_me:
                self.request.session.set_expiry(0)
            else:
                self.request.session.set_expiry(60 * 60 * 24 * 30)  # 30일
            if not user.is_active:
                messages.warning(self.request, "Your email is not verified. Please check your email.")
            else:
                messages.success(self.request, "Successfully logged in.")
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, "Invalid email or password.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["debug"] = settings.DEBUG
        return context


class LogOutView(View):
    def get(self, request: HttpRequest):
        try:
            logout(request)
            messages.success(request, "Successfully logged out.")
            return redirect("/")
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            messages.error(request, "Logout error.")
            return redirect("/")


class DeleteUserView(View):
    def post(self, request: HttpRequest):
        if not settings.DEBUG:
            return JsonResponse({"error": "Not allowed"}, status=403)

        form = DeleteUserForm(request.POST)
        if form.is_valid():
            try:
                user_uuid = form.cleaned_data["user_uuid"]
                user_model = get_user_model()
                user = user_model.objects.get(pk=user_uuid)
                user.delete()
                return redirect("accounts:signup")
            except Exception as e:
                return render(
                    request,
                    "accounts/signup_form.html",
                    {"form": form, "error": str(e)},
                )

        return redirect("accounts:signup")

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

class VerifyEmailView(View):
    def get(self, request: HttpRequest, uid: str, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        check_token = email_verification_token.check_token(user, token)
        if user is not None and check_token:
            user.is_active = True
            user.save()
            messages.success(request, "Email verification successful.")
            return redirect("/")
        else:
            messages.error(request, "Email verification failed.")
            return redirect("/")

def generate_random_otp(length=6):
    otp = "".join(str(random.randint(0, 9)) for _ in range(length))
    return otp

class PasswordResetEmailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializer.UserSerializer
    
    def get_object(self):
        email = self.kwargs.get("email")
        user = User.objects.filter(email=email).first()
        
        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            
            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()
            
            link = f"{settings.FRONTEND_URL}/password-reset/{uuidb64}/{user.otp}"
            logger.info(f"Password reset link: {link}")
            
            context = {
                "link": link,
                "username": user.username,
            }
            
            subject = "Password Reset"
            text_body = render_to_string("accounts/password_reset_email.txt", context)
            html_body = render_to_string("accounts/password_reset_email.html", context)
            
            from_email = settings.DEFAULT_FROM_EMAIL
            
            msg = EmailMultiAlternatives(subject, text_body, from_email, [user.email])
            msg.attach_alternative(html_body, "text/html")
            msg.send()
            
            return user
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class PasswordChangeView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializer.UserSerializer
    
    def create(self, request: HttpRequest, *args, **kwargs):
        otp = request.data.get("otp")
        uuidb64 = request.data.get("uuidb64")
        password = request.data.get("password")
        
        user = User.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)