from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        results = [
            {
                'title': 'Beautiful is better than ugly',
                'author': 'John Doe',
                'content': 'Beautiful is better than ugly',
                'published_at': 'October 1, 2022'
            },
            {
                'title': 'Explicit is better than implicit',
                'author': 'Jane Doe',
                'content': 'Explicit is better than implicit',
                'published_at': 'October 1, 2022'
            }
        ]
        context = {
            "info": results,
            "title": "Python Test"
        }
        return render(request, "demo/home.html", context)
