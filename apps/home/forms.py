from django import forms

class QRCommonOptionsForm(forms.Form):
    """QR 코드 공통 옵션을 위한 폼"""
    STYLE_CHOICES = [
        ('SQUARE_MODULE', 'Square'),
        ('ROUNDED_MODULE', 'Rounded'),
        ('VERTICAL_BARS', 'Vertical Bars'),
        ('HORIZONTAL_BARS', 'Horizontal Bars'),
    ]

    COLOR_MASK_CHOICES = [
        ('SOLID_FILL', 'Solid Fill'),
        ('RADIAL_GRADIENT', 'Radial Gradient'),
        ('SQUARE_GRADIENT', 'Square Gradient'),
        ('HORIZONTAL_GRADIENT', 'Horizontal Gradient'),
        ('VERTICAL_GRADIENT', 'Vertical Gradient'),
    ]

    style = forms.ChoiceField(
        choices=STYLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    color_mask = forms.ChoiceField(
        choices=COLOR_MASK_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fill_color = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'form-control form-control-color',
            'value': '#000000'
        })
    )
    back_color = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'form-control form-control-color',
            'value': '#FFFFFF'
        })
    )
    embedded_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    embedded_image_ratio = forms.FloatField(
        min_value=0.1,
        max_value=0.5,
        initial=0.25,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'class': 'form-range',
            'step': '0.05'
        })
    )

class URLQRForm(QRCommonOptionsForm):
    """URL QR 코드 생성 폼"""
    url = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com'
        })
    )

class TextQRForm(QRCommonOptionsForm):
    """텍스트 QR 코드 생성 폼"""
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3'
        })
    )

class EmailQRForm(QRCommonOptionsForm):
    """이메일 QR 코드 생성 폼"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3'
        })
    )

class PhoneQRForm(QRCommonOptionsForm):
    """전화번호 QR 코드 생성 폼"""
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+11001001000'
        })
    )

class SMSQRForm(PhoneQRForm):
    """SMS QR 코드 생성 폼"""
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3'
        })
    )

class WhatsAppQRForm(SMSQRForm):
    """WhatsApp QR 코드 생성 폼"""
    pass

class WiFiQRForm(QRCommonOptionsForm):
    """WiFi QR 코드 생성 폼"""
    ENCRYPTION_CHOICES = [
        ('WPA', 'WPA/WPA2'),
        ('WEP', 'WEP'),
        ('nopass', 'None'),
    ]

    ssid = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    encryption = forms.ChoiceField(
        choices=ENCRYPTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    hidden = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class VCardQRForm(QRCommonOptionsForm):
    """VCard QR 코드 생성 폼"""
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    vcard_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    vcard_mobile = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    organization = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    job_title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    vcard_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )