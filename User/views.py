from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, PasswordChangeForm
from .models import User


class user_login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'User/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if self.request.user.is_superuser:
                    return redirect('survey:management')
                return redirect('survey:home')
        return render(request, 'User/login.html', {'form': form, 'error': True})


class user_logout(View):
    def get(self, request):
        logout(request)
        return redirect('user:login')


class User_edit(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            user = User.objects.get(id=self.request.user.id)
            form = PasswordChangeForm(request.user, request.POST)
            return render(request, 'User/edit.html', {'form': form, 'user': user})
        
    def post(self, request):
        if self.request.user.is_authenticated:
            form = PasswordChangeForm(request.user, request.POST)
            user = User.objects.get(id=self.request.user.id)
            if form.is_valid():
                form.save()
                return redirect('user:login')
            else:
                if form.errors.get('old_password'):
                    message = 'رمز عبور فعلی نادرست است.'
                elif form.data.get('new_password1') != form.data.get('new_password2'):
                    message = 'رمز عبور جدید با تکرار آن برابر نیست.'
                elif form.errors.get('new_password2'):
                    message = 'رمز عبور جدید مطابق با الگوی رمز امن نیست.'
                return render(request, 'User/edit.html', {'form': form, 'user': user, 'status': False, 'message': message})
