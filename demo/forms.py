from django.forms import ModelForm

from demo.models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author', 'author']
