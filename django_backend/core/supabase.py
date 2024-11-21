from django.conf import settings
from supabase import create_client, Client

supabase: Client = create_client(settings.SUPABASE_API_URL, settings.SUPABASE_ANON_KEY)
