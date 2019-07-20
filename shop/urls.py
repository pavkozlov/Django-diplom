from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('category/<id>/', views.category, name='category'),
    path('item/<id>/', views.item_detail, name='item_detail'),
    path('item/<item_id>/add_review', views.add_review, name='add_review'),
    path('basket/', views.basket_view, name='basket_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


