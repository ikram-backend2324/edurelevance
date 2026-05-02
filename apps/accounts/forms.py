from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'cyber-input',
            'placeholder': 'Email manzilingiz'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'cyber-input',
            'placeholder': 'Foydalanuvchi nomi'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'cyber-input',
            'placeholder': 'Parol'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'cyber-input',
            'placeholder': 'Parolni tasdiqlang'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'cyber-input',
            'placeholder': 'Foydalanuvchi nomi'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'cyber-input',
            'placeholder': 'Parol'
        })
    )
