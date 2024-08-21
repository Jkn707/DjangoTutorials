from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.shortcuts import render, redirect
# Create your views here.
class homePageView(TemplateView):
    template_name = 'pages\home.html'

class aboutPageView(TemplateView):
    template_name = 'pages/about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle1": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })
        return context
    
class contactPageView(TemplateView):
    template_name = 'pages/contact.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle1": "Contact us",
            "email": "onlinestore@gmail.com",
            "phone": "+1234567890",
            "address": "1234 Main St, City, Country"
        })
        return context
    
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 1000},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 800},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 50},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 100},
    ]
class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)
class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        if int(id) > len(Product.products):
            return redirect("home")
        viewData = {}
        product = Product.products[int(id)-1]
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)
    
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("Price must be greater than 0")


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
            return redirect("success")
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        
class ProductCreateSuccessView(TemplateView):
    template_name = 'products/success.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Product created",
            "subtitle": "Product created successfully",
        })
        return context
