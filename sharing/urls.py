from django.urls import path

from . import views

app_name = "sharing"
urlpatterns = [
    path("<uuid:token>/note/", views.shared_note, name="note"),
]
