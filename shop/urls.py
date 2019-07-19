from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('category/<id>/', views.category, name='category'),
    path('item/<id>/', views.item_detail, name='item_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


