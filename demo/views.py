from django.shortcuts import render
from django.views import View

from demo.models import Article


class HomeView(View):
    def get(self, request):
        results = Article.objects.all()
        context = {
            "info": results,
            "title": "Python Test"
        }
        return render(request, "demo/home.html", context)
