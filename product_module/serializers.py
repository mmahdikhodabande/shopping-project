from rest_framework import serializers

from product_module.models import Product


class models_serializer_product(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
