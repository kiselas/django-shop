from django.urls import path
from .views import (BaseView,
                    ProductDetailView,
                    CategoryDetailView,
                    CartView,
                    AddToCartView,
                    DeleteFromCartView,
                    ChangeQTYView
                    )

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path("products/<str:ct_model>/<str:slug>/", ProductDetailView.as_view(), name='product_detail'),
    path('products/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:ct_model>/<str:slug>', DeleteFromCartView.as_view(), name='del_from_cart'),
    path('change_qty/<str:ct_model>/<str:slug>', ChangeQTYView.as_view(), name='change_qty')
]
