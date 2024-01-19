from django import forms


class ManagementForm(forms.Form):
    user_file = forms.FileField(widget=forms.PasswordInput(
        attrs={'type': 'file', 'class': 'form-control'}))
