
from rest_framework import serializers
from api.models import *
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password'] 
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
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
    

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)  
    
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


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested Product Data (no recursion here)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'qty', 'sub_total']

    def get_sub_total(self, obj):
        return obj.sub_total()


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)  # Avoids recursion
    user = UserSerializer(read_only=True) 
    total_price = serializers.SerializerMethodField()  

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'payment_type', 'shipping_address', 'created_at', 'order_items']

    def get_total_price(self, obj):
        return obj.total_order_price()

