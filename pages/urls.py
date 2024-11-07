from django.urls import path
from .views import HomePageView, AboutPageView, ContactPageView, ProductIndexView, ProductShowView, ProductCreateView, CartView, CartRemoveAllView
from .views import ImageViewFactory, ImageViewNoDI
from .utils import ImageLocalStorage

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
	path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'), # ACTIVIDAD 1.
	path('products/', ProductIndexView.as_view(), name='index'), # Para ver ACTIVIDAD 2, ir a base.html y buscando la línea 27.
	path('products/create', ProductCreateView.as_view(), name='form'),
	path('products/<str:id>', ProductShowView.as_view(), name='show'),
	
	# TUTORIAL 6A
	path('cart/', CartView.as_view(), name='cart_index'),
	path('cart/add/<str:product_id>', CartView.as_view(), name='cart_add'),
	path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
	
	# TUTORIAL 6B

    path('image/', ImageViewFactory(ImageLocalStorage()).as_view(), name='image_index'),
    path('image/save', ImageViewFactory(ImageLocalStorage()).as_view(), name='image_save'),
    
    # TUTORIAL 6-B -- SAME APPLICATION WITHOUT DEPENDENCY INVERSION
    path('imagenotdi/', ImageViewNoDI.as_view(), name='imagenodi_index'),
	path('image/save', ImageViewNoDI.as_view(), name='imagenodi_save'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
