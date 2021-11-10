from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect, render

from api.forms import CreateUserForm


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for ${user}")
            return redirect("/auth/token")

    context = {"form": form}
    return render(request, "auth/register.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("/auth/token")
        else:
            messages.info(request, "Username or password incorrect")
    return render(request, "auth/login.html", {})


def home(request):
    context = {"boldmessage": "Hello world"}

    return render(request, "index.html", context)


def logout_view(request):
    logout(request)
    return redirect("/login")
