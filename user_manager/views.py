from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView


def index(request):
    return render(request, "user_manager/index.html")


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("user_manager:index")
    template_name = "user_manager/register.html"


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    success_url = reverse_lazy("user_manager:index")
    template_name = "user_manager/login.html"


class UserLogoutView(LogoutView):
    pass
