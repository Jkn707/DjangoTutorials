from django.urls import path
from .views import (HomePageView, AboutPageView, ProductIndexView, 
                    ProductShowView, ProductCreateView, ProductCreateSuccessView, 
                    CartView, CartRemoveAllView, ImageDIView
                    )
from .utils import ImageLocalStorage

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('products/', ProductIndexView.as_view(), name='index'),
    path('products/create', ProductCreateView.as_view(), name='form'),
    path('products/<str:id>', ProductShowView.as_view(), name='show'),
    path('products/product-created', ProductCreateSuccessView.as_view(), name='product-created'),
    path('cart/', CartView.as_view(), name='cart_index'),
    path('cart/add/<str:product_id>', CartView.as_view(), name='cart_add'),
    path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
    path('imagesdi/', ImageDIView.as_view(), name='imagesdi_index'),
    path('imagesdi/save', ImageDIView.as_view(), name='imagesdi_save'),
]
