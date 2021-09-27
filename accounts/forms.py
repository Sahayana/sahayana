from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    nickname = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'nickname', 'email')

class CustomUserChangeForm(UserChangeForm):
    nickname = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'nickname', 'email')