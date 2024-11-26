from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils.translation import gettext as _

from utils import SuccessMessageMixin
from .forms import LoginUserForm


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    extra_context = {'title': _("Log In"), 'button': _("Enter")}
    success_url = reverse_lazy('home')
    success_message = _('You are logged in')


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(self.request, _('You are logged out'))
        return redirect('home')
