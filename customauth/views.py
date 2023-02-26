from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views import View

from customauth.serializers import LoginForm


class HomeView(View):
    def get(self, request: HttpRequest):
        # 如果用户已经登陆重定向到首页
        if request.user.is_authenticated:
            messages.success(request, 'You are logged in!')
            return redirect(reverse("mydemo:home"))
        context = {
            "form": LoginForm()
        }
        return render(request, "customauth/login.html", context)

    def post(self, request):
        data = LoginForm(data=request.POST)
        if data.is_valid():
            username = data.cleaned_data['username']
            password = data.cleaned_data['password']

            # authenticate函数验证用户名字和密码
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Hi %s, Welcome back!' % user.username.title())
                return redirect('mydemo:home')

        messages.error(request, 'Invalid username or password!')
        return render(request, 'customauth/login.html', {'form': data})


class LogOutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('myauth:login')
