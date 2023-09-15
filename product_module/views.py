from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView
from utils.http_service import http_client_ip
from .models import Product, ProductCategory, ProductBrand, product_visit, gallery_product
from django.http import HttpRequest
from django.db.models import Count
from site_module.models import ads_baner
from utils.convertors import slider_list
from rest_framework import generics

from .serializers import models_serializer_product


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 2

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        name_category = self.kwargs.get('cat')
        name_brand = self.kwargs.get('brand')
        if name_brand is not None:
            query = query.filter(brand__url_title__iexact=name_brand)

        if name_category is not None:
            query = query.filter(category__url_title__iexact=name_category)

        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baner_ADS'] = ads_baner.objects.filter(is_active=True,
                                                        position__iexact=ads_baner.baner_position.product_list)
        return context


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get("product_favorites")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['product_brand'] = slider_list(list(Product.objects.filter(
            brand_id=loaded_product.brand_id).all())[:7], 3)
        context['gallery_product'] = slider_list(
            list(gallery_product.objects.filter(product_id=loaded_product.id).all()), 3)
        user_ip = http_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = product_visit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

        if not has_been_visited:
            new_visit = product_visit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context


class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product_favorites"] = product_id
        return redirect(product.get_absolute_url())


def category_component_product(request: HttpRequest):
    category_product = ProductCategory.objects.filter(is_active=True, is_delete=False)
    product_brand = ProductBrand.objects.filter(is_active=True)
    count_brand_product = ProductBrand.objects.count()
    context = {
        'product': category_product,
        'brand_product': product_brand,
        'count_of_product': count_brand_product
    }
    return render(request, 'component/category_component_product.html', context)


def brand_component_product(request: HttpRequest):
    product_brand = ProductBrand.objects.annotate(brand_count=Count('product')).filter(is_active=True)
    context = {
        'brand_product': product_brand
    }
    return render(request, 'component/brand_products.html', context)


class serializer_product(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('price').all()
    serializer_class = models_serializer_product


class serializer_product_delete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.order_by('price').all()
    serializer_class = models_serializer_product
