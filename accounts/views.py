from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from lab.flags import compute_flag

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import Profile
from .ui_prefs import COOKIE_NAME, decode_prefs, default_prefs, encode_prefs
from .remember import COOKIE_NAME as REMEMBER_COOKIE
from .remember import MAX_AGE_SECONDS, make_token


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            role = "seller" if form.cleaned_data["as_seller"] else "customer"
            Profile.objects.create(user=user, role=role)
            login(request, user)
            messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli.")
            return redirect("shop:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                response = redirect("shop:home")
                if form.cleaned_data["remember"]:
                    response.set_cookie(
                        REMEMBER_COOKIE, make_token(user.username),
                        max_age=MAX_AGE_SECONDS, httponly=False,
                    )
                messages.success(request, "Xush kelibsiz!")
                return response
            messages.error(request, "Login yoki parol noto'g'ri.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    response = redirect("shop:home")
    response.delete_cookie(REMEMBER_COOKIE)
    return response


@login_required
def profile(request):
    prof, _ = Profile.objects.get_or_create(user=request.user, defaults={"role": "customer"})
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            prof.phone = form.cleaned_data["phone"]
            prof.address = form.cleaned_data["address"]
            prof.save()
            messages.success(request, "Profil yangilandi.")
    else:
        form = ProfileForm(initial={"phone": prof.phone, "address": prof.address})

    flag = None
    if prof.role == "admin":
        flag = compute_flag("A04-CRYPTO")

    return render(request, "accounts/profile.html", {"form": form, "profile": prof, "flag": flag})


@login_required
def beta_tools(request):
    raw = request.COOKIES.get(COOKIE_NAME)
    prefs = decode_prefs(raw) if raw else None
    is_admin_via_cookie = bool(prefs and prefs.get("role") == "admin")

    flag = compute_flag("A08-INTEGRITY") if is_admin_via_cookie else None
    response = render(request, "accounts/beta_tools.html", {
        "is_admin_via_cookie": is_admin_via_cookie,
        "flag": flag,
    })
    if not raw:
        prof, _ = Profile.objects.get_or_create(user=request.user, defaults={"role": "customer"})
        response.set_cookie(COOKIE_NAME, encode_prefs(default_prefs(prof.role)))
    return response
