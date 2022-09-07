from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from product.mixins import SerializerByMethodMixin
from product.models import Product
from product.permissions import IsSellerAndOwnerOrReadOnly, IsSellerOrReadOnly
from product.serializers import CreateProductSerializer, ListProductSerializer


class ListCreateProductView(SerializerByMethodMixin ,generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsSellerOrReadOnly]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ListProductSerializer,
        "POST": CreateProductSerializer,
    }

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)

class RetrieveUpdateProductView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsSellerAndOwnerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ListProductSerializer
    serializer_map = {
        "GET": ListProductSerializer,
        "PATCH": CreateProductSerializer,
    }