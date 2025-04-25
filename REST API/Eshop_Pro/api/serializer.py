from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import *
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create the user
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        token, _ = Token.objects.get_or_create(user=user)               # Ensure only one token per user
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['category'] = CategorySerializer(instance.category).data
        return resp

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['user'] = UserSerializer(instance.user).data
        return resp
    
class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = "__all__"
    
    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['cart'] = CartSerializer(instance.cart).data
        resp['product'] = ProductSerializer(instance.product).data
        return resp 

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['user'] = UserSerializer(instance.user).data
        return resp
    
class OrderItemSerializer(serializers.ModelSerializer):
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "qty", "price_at_purchase", "sub_total"]

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['order_id'] = instance.order.id                        # Avoid recursion by returning order ID instead of full order
        resp['product'] = ProductSerializer(instance.product).data
        return resp

    def get_sub_total(self, obj):
        return obj.sub_total()


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True) 
    user = UserSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['user'] = UserSerializer(instance.user).data
        resp['shipping_address'] = AddressSerializer(instance.shipping_address).data
        return resp

    def get_total_price(self, obj):
        return obj.total_order_price()
