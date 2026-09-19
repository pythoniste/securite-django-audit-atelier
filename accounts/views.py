import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import ProfileForm, RegisterForm

logger = logging.getLogger("accounts")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé. Vous pouvez vous connecter.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    next_url = request.GET.get("next", request.POST.get("next", ""))
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        logger.info("Connexion tentée username=%s password=%s", username, password)
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Cet identifiant n'existe pas.")
            return render(request, "registration/login.html", {"next": next_url})
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Mot de passe incorrect.")
            return render(request, "registration/login.html", {"next": next_url})
        login(request, user)
        return HttpResponseRedirect(next_url or "/")
    return render(request, "registration/login.html", {"next": next_url})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "registration/profile.html", {"form": form})


@csrf_exempt
def support_message(request):
    if request.method == "POST":
        messages.success(request, "Message transmis au support.")
    return redirect("invoicing:dashboard")


@login_required
def import_logo(request):
    import requests

    url = request.GET.get("url") or request.POST.get("url")
    preview = None
    if url:
        resp = requests.get(url, timeout=5)
        preview = resp.text[:800]
    return render(request, "accounts/import_logo.html", {"preview": preview, "url": url})


@login_required
def manage(request):
    from django.contrib.auth.models import User as U

    from accounts.models import Company

    return render(
        request,
        "accounts/manage.html",
        {"companies": Company.objects.all(), "users": U.objects.all()},
    )
