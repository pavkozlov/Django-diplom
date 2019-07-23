from django.contrib import admin
from .models import Item, Article, Category, Review, ItemInBasket, Basket, Order, ItemInOrder

# Register your models here.
admin.site.register(Item)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ItemInBasket)
admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(ItemInOrder)