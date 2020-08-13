from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class UserEmailEdit(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = "accounts/edit_email.html"
    fields = ["email", ]

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("user_detail", args=[self.request.user.username])


class UserProfileUpdate(generic.UpdateView):
    model = User
    template_name = 'accounts/edit.html'
    fields = ["username", "first_name", "last_name", ]

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("user_detail", args=[self.request.user.username])
