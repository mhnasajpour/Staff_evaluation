from django import forms
from django.contrib.auth.forms import PasswordChangeForm as PassChangeForm
from django.contrib.auth import password_validation

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'}))
    

class PasswordChangeForm(PassChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'}))