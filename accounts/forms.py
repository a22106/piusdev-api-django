from django import forms
from django.contrib.auth import get_user_model

class SignUpForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "name@example.com"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_model = get_user_model()
        if user_model.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

class DeleteUserForm(forms.Form):
    user_uuid = forms.UUIDField(widget=forms.HiddenInput())

class SignInForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "name@example.com"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean(self):
        cleaned_data = super().clean()
        # 추가적인 검증 로직 여기에 추가
        return cleaned_data