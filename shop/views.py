from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Article, Item, Review, Basket, ItemInBasket
from .forms import AddReview
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


# Create your views here.
def mainpage(request):
    context = dict()
    context['categories'] = get_categories()
    context['articles'] = Article.objects.all().prefetch_related('items').order_by('id')
    return render(request, 'shop/index.html', context=context)


def category(request, id):
    context = dict()
    context['categories'] = get_categories()
    context['category'] = get_object_or_404(Category, id=id)
    context['cat_name'] = context['category'].title
    return render(request, 'shop/category.html', context=context)


def item_detail(request, id):
    context = dict()
    context['forms'] = AddReview()
    context['categories'] = get_categories()
    context['item'] = get_object_or_404(Item, id=id)
    return render(request, 'shop/item_detail.html', context=context)


def add_review(request, item_id):
    form = AddReview(request.POST)
    if form.is_valid():
        Review.objects.create(name=form.cleaned_data['name'], text=form.cleaned_data['text'],
                              star=form.cleaned_data['star'], item=Item.objects.get(id=item_id))
    return redirect('item_detail', id=item_id)


def basket_view(request):
    context = dict()
    context['categories'] = get_categories()
    context['basket'] = ItemInBasket.objects.filter(basket=get_basket(request)).select_related('item')
    return render(request, 'shop/basket.html', context=context)


def to_basket(request, item_id):
    basket = get_basket(request)
    item = Item.objects.get(id=item_id)

    item_in_basket = ItemInBasket.objects.filter(basket=basket, item=item)

    if item_in_basket:
        my_obj = item_in_basket.first()
        my_obj.count += 1
        my_obj.save()
    else:
        ItemInBasket.objects.create(basket=basket, item=item, count=1)
    return redirect(basket_view)


def get_basket(request):
    sid = request.session.session_key
    if not sid:
        request.session.cycle_key()
        sid = request.session.session_key

    basket = Basket.objects.filter(sid=sid)
    if not basket:
        basket = Basket.objects.create(sid=sid)
    else:
        basket = basket.first()
    return basket


def get_categories():
    categories = cache.get_or_set('categories', Category.objects.filter(is_main=True), 3600)
    return categories


def clear_authors_count_cache():
    cache.delete('categories')


@receiver(post_delete, sender=Article)
def category_post_delete_handler(sender, **kwargs):
    clear_authors_count_cache()


@receiver(post_save, sender=Article)
def category_post_save_handler(sender, **kwargs):
    if kwargs['created']:
        clear_authors_count_cache()
