from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserSignUpForm
User = get_user_model()


class SignUp(generic.CreateView):
    form_class = UserSignUpForm
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


class UserProfileUpdate(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'accounts/edit.html'
    fields = ["username", "first_name", "last_name", ]

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("user_detail", args=[self.request.user.username])


def dark_mode_toggle(request):
    current = request.session.get("darkmode", "")
    request.session["darkmode"] = not current
    return HttpResponse(current)
