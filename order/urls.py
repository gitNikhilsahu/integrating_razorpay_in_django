from django.urls import path
from .views import order_view, success_view, order_api_view

urlpatterns = [
    path('', order_view, name='order'),
    path('success' , success_view , name='success'),
    path('order/api', order_api_view, name='order-api')
]