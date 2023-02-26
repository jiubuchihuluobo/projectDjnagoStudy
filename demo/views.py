from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from demo.forms import ArticleForm
from demo.models import Article


class HomeView(View):
    def get(self, request: HttpRequest):
        results = Article.objects.all()
        context = {
            "info": results,
            "title": "Python Test"
        }
        return render(request, "demo/home.html", context)


class CreateView(View):
    def get(self, request: HttpRequest):
        context = {
            "form": ArticleForm()
        }
        return render(request, "demo/create.html", context)

    def post(self, request: HttpRequest):
        data = ArticleForm(request.POST)
        if data.is_valid():
            data.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect("demo:home")
        else:
            messages.error(request, 'Please correct the following errors.')
            return render(request, "demo/create.html", context={"form": data})
