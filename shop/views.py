from django.shortcuts import render, get_object_or_404
from .models import Category, Article, Item
from .forms import AddReview


# Create your views here.
def mainpage(request):
    context = dict()
    context['categories'] = Category.objects.filter(is_main=True)
    context['articles'] = Article.objects.all().prefetch_related('items').order_by('id')
    return render(request, 'shop/index.html', context=context)


def category(request, id):
    context = dict()
    categories = Category.objects.all()
    context['category'] = get_object_or_404(categories, id=id)
    context['categories'] = categories.filter(is_main=True)
    return render(request, 'shop/category.html', context=context)


def item_detail(request, id):
    context = dict()
    context['forms'] = AddReview()
    context['categories'] = Category.objects.filter(is_main=True)
    context['item'] = get_object_or_404(Item, id=id)
    return render(request, 'shop/item_detail.html', context=context)
