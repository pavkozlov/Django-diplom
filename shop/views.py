from django.shortcuts import render
from .models import Category, Article


# Create your views here.
def mainpage(request):
    context = dict()
    context['categories'] = Category.objects.filter(is_main=True)
    context['articles'] = Article.objects.all()
    return render(request, 'shop/index.html', context=context)
