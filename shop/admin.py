from django.contrib import admin
from .models import Item, Article, Category

# Register your models here.
admin.site.register(Item)
admin.site.register(Article)
admin.site.register(Category)
