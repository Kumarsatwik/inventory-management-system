"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('items/', views.item_list, name='item_list'),
    path('order/', views.order_list, name='order_list'),
    path('transaction/', views.transaction_list, name='transaction_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/<int:pk>/', views.item_details, name='item_details'),
    path('sell/<int:pk>/', views.sell_item, name='sell_item'),
    path('edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('order/<int:pk>/', views.order_item, name='order_item'),
    path('edit_order/<int:pk>/', views.edit_order, name='edit_order'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
