import datetime
import os
import random

import django
from django.db.models import QuerySet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'permissionTest.settings')
django.setup()

from demo.models import Article
from customauth.models import User

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
for result in results:
    user = User.objects.filter(username=result.get("author"))
    if not user:
        user_info = {
            "username": result.get("author"),
            "email": "date21092%d@gmail.com" % random.randint(0, 100)
        }
        user = User.objects.create(**user_info)
    if isinstance(user, QuerySet):
        user = user[0]
    result.update({"author": user})
    result.update({"published_at": datetime.datetime.strptime(result.get("published_at"), "%B %d, %Y").strftime("%Y-%m-%d")})
    Article.objects.create(**result)
