from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from .models import Product
from django.urls import reverse
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
    
class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)
    

class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Invalid product id")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return redirect(reverse("home"))

        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)
    

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products - Online Store"
        context["subtitle"] = "List of products"
        return context
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

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
            form.save()
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
