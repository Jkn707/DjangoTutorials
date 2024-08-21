from django.urls import path
from .views import homePageView, aboutPageView, ProductIndexView, ProductShowView, ProductCreateView, contactPageView, ProductCreateSuccessView

urlpatterns = [
    path('', homePageView.as_view(), name="home"),
    path('about/', aboutPageView.as_view(), name="about"),
    path('products/', ProductIndexView.as_view(), name="index"),
    path('products/create/', ProductCreateView.as_view(), name="create"),
    path('products/<str:id>/', ProductShowView.as_view(), name="show"),
    path('contact/', contactPageView.as_view(), name="contact"),
    path('product/create/success/', ProductCreateSuccessView.as_view(), name="success"),
]