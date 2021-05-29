from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(ModelSerializer):
	class Meta:
		model = Product
		fields = "__all__"

	def validate_slug(self, slug):
		if not slug:
			raise serializers.ValidationError('slug is required')

		return slug
class CategorySerializer(ModelSerializer):
	class Meta:
		model = Category
		fields = "__all__"
