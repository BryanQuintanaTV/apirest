from rest_framework.decorators import api_view
from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from .models import Order, OrderProduct
from .serializers import OrderSerializer, OrderProductSerializer

# Class With All The Actions That Endpoints Going To Do
# {URL}/api/v1/rest
class OrderList(APIView):

    # GET {URL}/api/v1/ordenes
    def get(self, request, *args, **kwargs):
        orders = Order.objects.prefetch_related('order_products__product')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    # POST {URL}/api/v1/ordenes
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        # Verify the body data on the request are valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If the body data is not valid, returns a 400 Error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE {URL}/api/v1/ordenes
    # Method Not Allowed
    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# Class With All The Actions That Endpoints Going To Do
# {URL}/api/v1/rest/{id}/
class OrderDetail(APIView):

    # GET {URL}/api/v1/ordenes/{id}/
    def get(self, request, id):
        order = get_object_or_404(Order, pk=id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    # PATCH {URL}/api/v1/ordenes/{id}/
    def patch(self, request, id):
        order = get_object_or_404(Order, pk=id)
        serializer = OrderSerializer(order, data=request.data, partial=True)

        # Verify if data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        # ir data is invalid, return a 400 error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE {URL}/api/v1/ordenes/{id}/
    def delete(self, request, id):
        order = get_object_or_404(Order, pk=id)

        # Delete the order and return a success response
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



