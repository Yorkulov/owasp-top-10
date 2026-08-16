from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    as_seller = forms.BooleanField(
        required=False, label="Sotuvchi sifatida ro'yxatdan o'tish (o'z do'konimni ochaman)"
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu foydalanuvchi nomi band.")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    remember = forms.BooleanField(required=False)


class ProfileForm(forms.Form):
    phone = forms.CharField(max_length=32, required=False)
    address = forms.CharField(max_length=255, required=False)
