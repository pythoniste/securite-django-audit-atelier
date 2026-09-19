from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_edit, name="profile"),
    path("support/", views.support_message, name="support"),
    path("company/import-logo/", views.import_logo, name="import_logo"),
    path("manage/", views.manage, name="manage"),
]
