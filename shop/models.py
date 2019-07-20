from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    items = models.ManyToManyField('Item', related_name='articles', blank=True)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    photo = models.ImageField(upload_to='shop/photos')
    cathegory = models.ForeignKey('Category', related_name='items', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    name = models.CharField(max_length=150)
    text = models.TextField()
    star = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')


class Category(models.Model):
    title = models.CharField(max_length=150)
    is_main = models.BooleanField()
    main_category = models.ForeignKey('Category', related_name='sub_categories', on_delete=models.CASCADE, blank=True,
                                      null=True)

    def __str__(self):
        return self.title


class Basket(models.Model):
    sid = models.CharField(max_length=150)
    items = models.ManyToManyField(Item, through='ItemInBasket', related_name='basket')


class ItemInBasket(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    count = models.IntegerField()


class Order(models.Model):
    items = models.ManyToManyField(Item, through='ItemInOrder')


class ItemInOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.IntegerField()
