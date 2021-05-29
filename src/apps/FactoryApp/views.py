from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category


class ProductViewSet(viewsets.ModelViewSet):
	serializer_class = ProductSerializer
	queryset = Product.objects.all()

class CategoryViewSet(viewsets.ModelViewSet):
	serializer_class = CategorySerializer
	queryset = Category.objects.all()
