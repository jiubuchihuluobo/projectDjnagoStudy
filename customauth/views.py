from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from customauth.serializers import LoginForm, RegisterForm


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


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "customauth/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            # commit = False并不会立即保存到数据库
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect("demo:home")
        else:
            return render(request, template_name="customauth/register.html", context={"form": form})


class MyLoginView(LoginView):
    template_name = 'customauth/todo_login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todoapp:tasks')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class MyRegisterView(FormView):
    template_name = 'customauth/todo_register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todoapp:tasks')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)

        return super(MyRegisterView, self).form_valid(form)
