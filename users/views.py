from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.translation import gettext as _

from .forms import RegisterUserForm
from utils import SuccessMessageMixin


class UsersListView(ListView):
    model = get_user_model()
    template_name = 'users/users_show.html'
    extra_context = {'title': _('Users')}
    context_object_name = 'users'


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'form.html'
    extra_context = {'title': _('Registration'), 'button': _('Register')}
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')


class UserChangeView:
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if not request.user.is_active:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
        elif request.user.pk != pk:
            messages.error(request, _('You do not have permission to change another user.'))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UserChangeView, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'form.html'
    extra_context = {'title': _('Update user'), 'button': _('Update')}
    success_url = reverse_lazy('users')
    success_message = _('User is successfully updated')


class UserDeleteView(UserChangeView, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'form_delete.html'
    extra_context = {'title': _('Delete user'), 'button': _('Yes, delete')}
    success_url = reverse_lazy('users')
    success_message = _('User is successfully deleted')
