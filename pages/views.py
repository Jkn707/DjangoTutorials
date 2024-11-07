from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from pages.utils import ImageLocalStorage, ImagesLocalStorage, ImageProvider
# from google.cloud import storage as gcs_storage
from django.conf import settings
from django.core.files.storage import default_storage

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'pages/home.html'



class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Nicolás Ramírez",
        })

        return context


class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] =  "List of products"
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        # Check if product id is valid
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
        except (ValueError, IndexError):
            # If the product id is not valid, redirect to the home page
            return HttpResponseRedirect(reverse('home'))
       
        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] =  product.name + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price


class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-created') 
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
    
        
class ProductCreateSuccessView(TemplateView):
    template_name = 'products/product-created.html'


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context


class CartView(View):
    template_name = 'cart/index.html'
        
    def get(self, request, *args, **kwargs):
        # Simulated database for products
        products = {}
        products[121] = {'name': 'Tv samsung', 'price': '1000'}
        products[11] = {'name': 'Iphone', 'price': '2000'}

        # Get cart products from session
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Prepare data for the view
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        # Get cart products from session and add the new product
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')


class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('cart_index')



class ImageBasicView(View):
    template_name = 'imagesbasic/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request):
        storage_type = request.POST.get('storage')

        if 'profile_image' in request.FILES:
            if storage_type == 'local':
                # Local storage
                profile_image = request.FILES.get('profile_image')
                if profile_image:
                    # Store the image
                    file_name = default_storage.save('uploaded_images/' + profile_image.name, profile_image)
                    image_url = default_storage.url(file_name)
                    request.session['image_url'] = image_url
                
            # elif storage_type == 'gcp':
            #     # GCP storage
            #     profile_image = request.FILES['profile_image']
            #     client = gcs_storage.Client.from_service_account_json(settings.GCP_KEY_FILE)
            #     bucket = client.bucket(settings.GCP_BUCKET)
            #     blob = bucket.blob('images/test.png')
            #     blob.upload_from_file(profile_image)
            else:
                 return HttpResponseRedirect(reverse('imagebasic_index'))


        return HttpResponseRedirect(reverse('imagebasic_index'))

class ImageDIView(View):
    template_name = 'imagesdi/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request):
        storage_type = request.POST.get('storage')
        profile_image = request.FILES.get('profile_image')
        provider = ImageProvider()
        if not profile_image:
            return HttpResponseRedirect(reverse('imagesdi_index'))

        imageStorage = provider.get_instance(storage_type)
        image_url = imageStorage.store(profile_image)

        if image_url:
            request.session['image_url'] = image_url

        return HttpResponseRedirect(reverse('imagesdi_index'))

