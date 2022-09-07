from rest_framework import serializers
from users.serializer import DetailUserSerializer

from product.models import Product


class ListProductSerializer(serializers.ModelSerializer):

    class Meta():
        model = Product
        fields = ["description", "price", "quantity", "is_active", "seller_id"]

class CreateProductSerializer(serializers.ModelSerializer):

    seller = DetailUserSerializer(read_only=True)

    class Meta():
        model = Product
        fields = ['id','seller', 'description', 'price', 'quantity', 'is_active' ]
        read_only_fields = ["seller_id","seller","is_active"]