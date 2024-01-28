from django import forms


class User_form(forms.Form):
    user_file = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'class': 'form-control'}))

class Question_form(forms.Form):
    question_file = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'class': 'form-control'}))
