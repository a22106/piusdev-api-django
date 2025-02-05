from django.contrib import admin
from .models import User, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'country', 'date')

admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)

