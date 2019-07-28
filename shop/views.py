from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Article, Item, Review, Basket, ItemInBasket, ItemInOrder, Order
from .forms import AddReview
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.paginator import Paginator


# Домашнаяя страница. Категории для меню берем из кэша / пишем в кэш. get_sid необходимо для того,
# что бы появился session_key (пропадает после logout, редирект  после выхода идёт на домашнюю страницу.
# Приходится его тут генерировать). Запросы к БД оптимизированы.
def mainpage(request):
    context = dict()
    get_sid(request)
    context['categories'] = get_categories()
    context['articles'] = Article.objects.all().prefetch_related('items').order_by('id')
    return render(request, 'shop/index.html', context=context)


# Страница с товарами определённой категории. Запросы к БД оптимизированы. cat (имя категории) получаем для того,
# что бы подсветить (сделать активным) нужный элемент меню
def category(request, id):
    context = dict()
    context['categories'] = get_categories()

    page = request.GET.get('page')
    page = 1 if not page else int(page)

    posts = Item.objects.filter(cathegory_id=id).select_related('cathegory')

    try:
        cat = posts[0].cathegory
    except IndexError:
        cat = Category.objects.get(id=id)

    paginator = Paginator(posts, 2)

    if page > paginator.num_pages:
        page = 1

    context['items'] = paginator.page(page)
    context['cat_name'] = cat.title
    return render(request, 'shop/category.html', context=context)


# Страница с подробным описанием товара
def item_detail(request, id):
    context = dict()
    context['forms'] = AddReview()
    context['categories'] = get_categories()
    context['item'] = get_object_or_404(Item, id=id)
    return render(request, 'shop/item_detail.html', context=context)


# Страница с корзиной.
# С помощью функции get_sid получаем ИМЯ ПОЛЬЗОВАТЕЛЯ или ID СЕССИИ
# По полученному значению находим корзмну с товарами / создаём новую корзину (если не существует)
# Получаем и передаём в шаблон все товары из корзины, с указанием их колличества (М2М связь).
# Запросы к БД оптимизированы
def basket_view(request):
    context = dict()
    context['categories'] = get_categories()
    basket = get_basket(get_sid(request))
    context['basket'] = ItemInBasket.objects.filter(basket=basket).select_related('item')
    return render(request, 'shop/basket.html', context=context)


# View для POST запроса. Добавляет отзыв к указанному товару, затем редиректит на этот товар
def add_review(request, item_id):
    form = AddReview(request.POST)
    if form.is_valid():
        Review.objects.create(name=form.cleaned_data['name'], text=form.cleaned_data['text'],
                              star=form.cleaned_data['star'], item=Item.objects.get(id=item_id))
    return redirect('item_detail', id=item_id)


# View для POST запроса. Добавляет товар нужным ID в корзину. Редирект на домашнюю страницу
def to_basket(request, item_id):
    basket = get_basket(get_sid(request))
    item = Item.objects.get(id=item_id)

    item_in_basket = ItemInBasket.objects.filter(basket=basket, item=item)

    if item_in_basket:
        my_obj = item_in_basket.first()
        my_obj.count += 1
        my_obj.save()
    else:
        ItemInBasket.objects.create(basket=basket, item=item, count=1)

    return redirect(basket_view)


# View для POST запроса. Оформляет заказ:
# 1) Получаем корзину исходя из ID сессии / username
# 2) Получаем все товары из корзины. Если их не 0:
# 3) Создаём заказ
# 4) Создаём m2m связь (Заказ, товар, колличество товара)
# 5) Удаляем m2m связь (Корзина, товар, колличество товара)
# Редирект на домашнюю страницу
# *iib означаем item in basket
def create_order(request):
    basket = get_basket(get_sid(request))
    items = basket.items.all()

    if items:
        order = Order.objects.create(owner=get_sid(request))
        for item in items:
            iib = ItemInBasket.objects.get(item=item, basket=basket)
            ItemInOrder.objects.create(item=item, order=order, count=iib.count)
            iib.delete()
    return redirect('mainpage')


# ВСПОМОГАТЛЬНЫЕ ФУНКЦИИ


# Находим или создаём новую корзину
def get_basket(sid):
    basket, created = Basket.objects.get_or_create(sid=sid)
    return basket


# Получаем имя пользователя (если авторизован) или его ID сессии
def get_sid(request):
    if not request.user.is_authenticated:
        sid = request.session.session_key
        if not sid:
            sid = request.session.cycle_key()
    else:
        sid = request.user.username
    return sid


# Получаем из кэша категории для меню. Если кэша нет, записываем их туда
def get_categories():
    categories = cache.get_or_set('categories', Category.objects.filter(is_main=True), 3600)
    return categories


# Удаление кэша
def clear_authors_count_cache():
    cache.delete('categories')


# Удаляется кэш, если удаляется одна из категорий
@receiver(post_delete, sender=Article)
def category_post_delete_handler(sender, **kwargs):
    clear_authors_count_cache()


# Удаляется кэш, если сохраняется одна из категорий
@receiver(post_save, sender=Article)
def category_post_save_handler(sender, **kwargs):
    if kwargs['created']:
        clear_authors_count_cache()
