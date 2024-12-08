from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# Class with all the actions to do with the endpoints
# {URL}/api/v1/productos/
class ProductList(APIView):

    # GET {URL}/api/v1/productos
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # POST {URL}/api/v1/productos/
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        # It verify if the data of the body in the request is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If data is not valid, returns a 400 Error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Class with all the actions to do with the endpoints
# {URL}/api/v1/productos/{id}/
class ProductDetail(APIView):

    # GET {URL}/api/v1/productos/{id}/
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PATCH {URL}/api/v1/productos/{id}/
    def patch(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        # Verify that data in the body of the request is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If data is not valid, returns a Error 400 response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE {URL}/api/v1/productos/{id}/
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
