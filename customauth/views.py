from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from customauth.serializers import LoginForm


class HomeView(View):
    def get(self, request):
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
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('demo:home')

        messages.error(request, 'Invalid username or password')
        return render(request, 'customauth/login.html', {'form': data})
