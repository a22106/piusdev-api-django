from django.urls import path

from calculator import views

urlpatterns = [
    path(route="", view=views.index, name="index"),
]
