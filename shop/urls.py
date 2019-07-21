from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('category/<id>/', views.category, name='category'),
    path('item/<id>/', views.item_detail, name='item_detail'),
    path('item/<item_id>/add_review', views.add_review, name='add_review'),
    path('item/<item_id>/to_basket', views.to_basket, name='to_basket'),
    path('basket/', views.basket_view, name='basket_view'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


