from django import forms
from django.contrib.auth.forms import PasswordChangeForm as PassChangeForm
from django.contrib.auth import password_validation

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control context-background'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control context-background'}))
    

class PasswordChangeForm(PassChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control context-background'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control context-background'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control context-background'}))