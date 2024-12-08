from rest_framework import serializers
from .models import Order, OrderProduct
from productos.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id_product', 'name_product', 'price_product', 'image_product')


class OrderProductSerializer(serializers.ModelSerializer):
    # Para GET: representación personalizada sin `product`
    id_product = serializers.IntegerField(write_only=True)  # Para POST y PATCH

    class Meta:
        model = OrderProduct
        fields = ('quantity', 'id_product')  # Campos para entrada y salida

    def to_representation(self, instance):
        """
        Personaliza la representación del GET para mostrar los campos requeridos.
        """
        return {
            'id_product': instance.product.id_product,
            'name_product': instance.product.name_product,
            'price_product': instance.product.price_product,
            'image_product': instance.product.image_product,
            'quantity': instance.quantity
        }

    def validate(self, data):
        """
        Validar que el producto exista al crear o actualizar.
        """
        try:
            Product.objects.get(pk=data['id_product'])
        except Product.DoesNotExist:
            raise serializers.ValidationError(f'El producto {data["id_product"]} no existe.')
        return data


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('num_order', 'total_order', 'date_order', 'id_user', 'order_products')

    def create(self, validated_data):
        """
        Crea una nueva orden junto con sus productos asociados.
        """
        order_products_data = validated_data.pop('order_products')  # Extrae los productos
        order = Order.objects.create(**validated_data)  # Crea la orden

        # Crea las relaciones de productos con la orden
        for order_product_data in order_products_data:
            product = Product.objects.get(pk=order_product_data['id_product'])
            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=order_product_data['quantity']
            )

        return order

    def update(self, instance, validated_data):
        """
        Actualiza una orden y sus productos asociados.
        """
        order_products_data = validated_data.pop('order_products', None)

        # Actualiza los campos de la orden
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if order_products_data:
            # Limpia las relaciones existentes antes de actualizar
            instance.order_products.all().delete()

            # Crea las nuevas relaciones
            for order_product_data in order_products_data:
                product = Product.objects.get(pk=order_product_data['id_product'])
                OrderProduct.objects.create(
                    order=instance,
                    product=product,
                    quantity=order_product_data['quantity']
                )

        return instance
