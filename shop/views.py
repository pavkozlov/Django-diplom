from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Article, Item, Review
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
    context['item'] = Item.objects.get(id=id)
    return render(request, 'shop/item_detail.html', context=context)


def add_review(request, item_id):
    form = AddReview(request.POST)
    if form.is_valid():
        item = Item.objects.get(id=item_id)
        Review.objects.create(name=form.cleaned_data['name'], text=form.cleaned_data['text'],
                              star=form.cleaned_data['star'], item=item)

    return redirect('item_detail', id=item_id)
