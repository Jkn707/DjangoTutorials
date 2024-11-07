from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .utils import ImageLocalStorage

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
            "author": "Developed by: Your Name",
        })

        return context
    
# ACTIVIDAD 1 - Adición de toda esta clase.
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Contact us",
            "application_email": "laempresa@hotmail.com",
            "address": "Calle 22 # 33-44",
            "phone_number": "(312) 456-7890",
        })
        
        return context
    

    # ACTIVIDAD 2 - Adición de productos en la barra de navegación (ver base.html).
    # ACTIVIDAD 3 - Adición de price en el diccionario de cada producto.
'''
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 1000}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 800},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 99},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 100},
    ]
'''

class ProductIndexView(View):
    template_name = 'products/index.html'
    
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        
        return render(request, self.template_name, viewData)
    

'''
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        # ACTIVIDAD 4 - Adición del Try - Except.
        try:
            product = Product.products[int(id)-1]
            viewData["title"] = product["name"] + " - Online Store"
            viewData["subtitle"] = product["name"] + " - Product information"
            viewData["product"] = product
            return render(request, self.template_name, viewData)
        except(IndexError, ValueError):
            messages.error(request, "Product ID not found")
            return HttpResponseRedirect(reverse('home'))
'''

## Tutorial 5
class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        # Check if product id is valid
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):# If the product id is not valid, redirect to the home page
            return HttpResponseRedirect(reverse('home'))
        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)





class ProductForm(forms.ModelForm):
    #name = forms.CharField(required=True)
    #price = forms.FloatField(required=True)
    
    # TUTORIAL 5
    
    class Meta:
        model = Product
        fields = ['name', 'price']
    
    
    # ACTIVIDAD 7 - Precio debe ser mayor a cero.
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class ProductCreateView(View):
    template_name = 'products/create.html'
    created_successful_template_name = 'products/created_successful.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)

        if form.is_valid():
            # TUTORIAL 5
            form.save()
            # ACTIVIDAD 8 - Producto creado exitosamente.
            return render(request, self.created_successful_template_name, {'title': 'Product created'})
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)


'''
class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        
        if form.is_valid():
            # Process the form data (save to database, etc.)
            # Example: 
            # product = Product.objects.create(name=form.cleaned_data['name'], price=form.cleaned_data['price'])

            # Redirect to a valid URL pattern name, e.g., 'product_list'
            return redirect('index')  # Replace 'product_list' with your actual URL pattern name
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)

'''

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' # This will allow you to loop through 'products' in your template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context

# TUTOTIAL 6-A
class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        # Simulated database for products
        products = {}
        products[1] = {'name': 'Johnson Ltd', 'price': '4899'}
        products[2] = {'name': 'Robertson-Owens', 'price': '4950'}
        products[19] = {'name': 'Tv samsung', 'price': '1000'}
        products[20] = {'name': 'Iphone', 'price': '2000'}
        
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

    def post(self, request, product_id):
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

# TUTORIAL 6-B
def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})
        
        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')
    return ImageView

# TUTORIAL 6-B -- SAME APPLICATION WITHOUT DEPENDENCY INVERSION
class ImageViewNoDI(View):
    template_name = 'images/index.html'
    
    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})
    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)
        request.session['image_url'] = image_url
        return redirect('image_index')
