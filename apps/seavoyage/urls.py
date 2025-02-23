
from django.urls import include, path
from .views import SeavoyageHelloView, SeavoyageView

app_name = "seavoyage"

urlpatterns = [
    path("", SeavoyageView.as_view(), name="seavoyage"),
]

