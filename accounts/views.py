from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from .forms import RegisterForm, RegistrationForm
from .models import Bookmark

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )

            return redirect("accounts:registration_complete")
        else:
            pass
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def registration_complete(request):
    return render(request, "accounts/registration_complete.html")


@login_required()
def profile(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    context = {"bookmarks": bookmarks}
    return render(request, "accounts/profile.html", context)
