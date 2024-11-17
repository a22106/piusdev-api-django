# accounts/utils.py
from django.contrib.auth.models import AnonymousUser

class SupabaseUser:
    def __init__(self, user_data):
        self.id = getattr(user_data, 'id', None)
        self.email = getattr(user_data, 'email', None)
        self.role = getattr(user_data, 'role', None)
        self.created_at = getattr(user_data, 'created_at', None)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True

    def get_username(self):
        return self.email

    def __str__(self):
        return self.email or ''