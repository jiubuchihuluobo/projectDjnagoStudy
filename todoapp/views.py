from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todoapp.models import Task


class HomeView(View):
    def get(self, request):
        return render(request, "todoapp/home.html")


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    # 指定要创建对象的类
    model = Task
    # 指定表单上显示的字段
    fields = ['title', 'description', 'completed']
    # 是任务成功创建后Django将重定向到的目标URL
    success_url = reverse_lazy('todoapp:tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The task was created successfully.")
        # 如果验证成功保存并重定向到success_url
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('todoapp:tasks')
    # 默认与CreateView公用一个视图，可以不设置
    template_name = "todoapp/task_form.html"

    def form_valid(self, form):
        messages.success(self.request, "The task was updated successfully.")
        return super(TaskUpdate, self).form_valid(form)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('todoapp:tasks')
