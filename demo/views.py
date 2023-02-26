from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from demo.models import Article
from demo.serializers import ArticleForm


class HomeView(View):
    def get(self, request: HttpRequest):
        results = Article.objects.all()
        context = {
            "info": results,
            "title": "Python Test"
        }
        return render(request, "demo/home.html", context)


@method_decorator(login_required, name='dispatch')
class CreateView(View):
    def get(self, request: HttpRequest):
        context = {
            "form": ArticleForm()
        }
        return render(request, "demo/create.html", context)

    def post(self, request: HttpRequest):
        # 反序列化
        data = ArticleForm(data=request.POST)
        if data.is_valid():
            data.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect("mydemo:home")
        else:
            messages.error(request, 'Please correct the following errors.')
            return render(request, "demo/create.html", context={"form": data})


@method_decorator(login_required, name='dispatch')
class EditView(View):
    def get(self, request: HttpRequest, pk):
        article = get_object_or_404(Article, id=pk)
        context = {
            "id": pk,
            # 序列化
            "form": ArticleForm(instance=article)
        }
        return render(request, "demo/create.html", context)

    def post(self, request: HttpRequest, pk):
        article = get_object_or_404(Article, id=pk)
        # 反序列化
        data = ArticleForm(data=request.POST, instance=article)
        if data.is_valid():
            data.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect("mydemo:home")
        else:
            messages.error(request, 'Please correct the following errors.')
            return render(request, "demo/create.html", context={"form": data})


@method_decorator(login_required, name='dispatch')
class DeleteView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        context = {
            "info": article
        }
        return render(request, "demo/delete.html", context)

    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        article.delete()
        messages.success(request, 'The post has been deleted successfully.')
        return redirect("mydemo:home")
