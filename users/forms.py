from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-label'}),
            'last_name': forms.TextInput(attrs={'class': 'form-label'}),
            'username': forms.TextInput(attrs={'class': 'form-label'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-label'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-label'}),
        }


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
