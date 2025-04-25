from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import generics, status
from api.models import *
from api.serializer import *


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    try:
        users = User.objects.all()
        s_users = UserSerializer(users, many=True)  # Serialize multiple users
        return Response({"users": s_users.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def registerUser(request):
    try:
        s_user = UserSerializer(data=request.data)
        if not s_user.is_valid():
            return Response({"data_errors": s_user.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = s_user.save()

        token = Token.objects.get(user=user)                    # Fetch the existing token (ensure one token per user)
        return Response({"message": "User registered successfully!", "token": token.key}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryAPI(APIView):
    def get(self, request):
        try:
            category_id = request.query_params.get('id')  # Get the 'id' from query parameters
            if category_id:
                category = get_object_or_404(Category, pk=category_id)
                s_category = CategorySerializer(category)
                return Response({"category": s_category.data}, status=status.HTTP_200_OK)
            
            # If no ID is provided, return all categories
            categories = Category.objects.all()
            s_categories = CategorySerializer(categories, many=True)
            return Response({"categories": s_categories.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            s_category = CategorySerializer(data=request.data)
            if not s_category.is_valid():
                return Response({"data_errors": s_category.errors}, status=status.HTTP_400_BAD_REQUEST)
            s_category.save()
            return Response({"message": "category added successfully!", "data": s_category.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        try:
            category = get_object_or_404(Category, pk=request.data['id'])
            s_category = CategorySerializer(category, data=request.data)
            if not s_category.is_valid():
                return Response({"data_errors": s_category.errors}, status=status.HTTP_400_BAD_REQUEST)
            s_category.save()
            return Response({"message": "category updated successfully!", "data": s_category.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request):
        try:
            category = get_object_or_404(Category, pk=request.data['id'])
            s_category = CategorySerializer(category)
            category.delete()
            return Response({"message": "category deleted successfully!", "data": s_category.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductAPI(APIView):
    def get(self, request):
        try:
            product_id = request.query_params.get('id')  # Get the 'id' from query parameters
            if product_id:
                product = get_object_or_404(Product, pk=product_id)
                s_product = ProductSerializer(product)
                return Response({"product": s_product.data}, status=status.HTTP_200_OK)
            
            # If no ID is provided, return all categories
            products = Product.objects.all()
            s_products = ProductSerializer(products, many=True)
            return Response({"product": s_products.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            s_products = ProductSerializer(data=request.data)
            if not s_products.is_valid():
                return Response({"data_errors": s_products.errors}, status=status.HTTP_400_BAD_REQUEST)
            s_products.save()
            return Response({"message": "product added successfully!", "data": s_products.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        try:
            product = get_object_or_404(Product, pk=request.data['id'])
            s_product = ProductSerializer(product, data=request.data)
            if not s_product.is_valid():
                return Response({"data_errors": s_product.errors}, status=status.HTTP_400_BAD_REQUEST)
            s_product.save()
            return Response({"message": "product updated successfully!", "data": s_product.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request):
        try:
            product = get_object_or_404(Product, pk=request.data['id'])
            s_product = ProductSerializer(product)
            product.delete()
            return Response({"message": "product deleted successfully!", "data": s_product.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartAPI(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            s_cart = CartSerializer(cart)
            return Response({"cart": s_cart.data}, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            product_id = int(request.data.get("product_id"))
            qty = int(request.data.get("quantity"))

            if not product_id or not qty:
                return Response({'error': 'product_id and qty are required'}, status=status.HTTP_400_BAD_REQUEST)

            product = get_object_or_404(Product, pk=product_id)

            if qty > product.productQty:
                return Response({"message":"Not Enough Quantity"}, status=status.HTTP_400_BAD_REQUEST)
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if created:
                cart_item.qty = qty
                cart_item.save()
                return Response({ 'message': 'Product added in cart', 'data': CartItemSerializer(cart_item).data }, status=status.HTTP_200_OK)
            else:
                cart_item.qty += qty
                cart_item.save()
                return Response({ 'message': 'Product already in cart, quantity updated', 'data': CartItemSerializer(cart_item).data }, status=status.HTTP_200_OK)
    
        except Exception as e:
             return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            cart.cart_items.all().delete()
            return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'500', 'errors':str(e), 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartItemAPI(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cartitem_id = request.query_params.get("id")
            if cartitem_id:
                cart_item = get_object_or_404(CartItem, pk=cartitem_id, cart__user=request.user)
                s_cart_item = CartItemSerializer(cart_item)
                return Response({"cart_item": s_cart_item.data}, status=status.HTTP_200_OK)

            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            s_cart_items = CartItemSerializer(cart_items, many=True)
            return Response({"cart_items": s_cart_items.data}, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        try:
            cart_item = get_object_or_404(CartItem, pk=request.data['cartitem_id'], cart__user=request.user)
            qty = request.data['quantity']

            cart_item.qty = qty
            cart_item.save()

            s_cart_item = CartItemSerializer(cart_item)
            return Response({"message": "cart item updated successfully!", "data": s_cart_item.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
             return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def delete(self, request):
        try:
            cartitem_id = request.data.get('cartitem_id') 
            if not cartitem_id:
                return Response({"error": "Cart item ID is required"}, status=400)

            cart_item = get_object_or_404(CartItem, id=cartitem_id, cart__user=request.user)
            s_cart_item = CartItemSerializer(cart_item)
            cart_item.delete()

            return Response({"message": "Item removed from cart", "data": s_cart_item.data}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class OrderAPI(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            order_id = request.query_params.get('id')
            if order_id:
                order = Order.objects.get(pk=order_id, user=request.user)
                s_order = OrderSerializer(order)
                return Response({"order": s_order.data}, status=status.HTTP_200_OK)
            
            orders = Order.objects.filter(user=request.user)
            if not orders.exists():
                return Response({'message': 'No Orders Yet!'}, status=status.HTTP_200_OK)
            
            s_orders = OrderSerializer(orders, many=True)
            return Response({"orders": s_orders.data}, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)

            if cart.cart_items.count() == 0:
                return Response({"message":"Cart is empty!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            payment_id = request.data.get('payment_id', None)
            payment_type = request.data.get('payment_type', 'cash on delivery')
            shipping_address_id = request.data.get('shipping_address', 1)            
            try:
                shipping_address = Address.objects.get(id=shipping_address_id)
            except Address.DoesNotExist:
                return Response({"error": "Invalid shipping address."}, status=status.HTTP_404_NOT_FOUND)
            
            total_price = cart.total_cart_price()

            order = Order.objects.create(
                user=request.user, 
                total_price=total_price, 
                payment_id=payment_id, 
                payment_type=payment_type, 
                shipping_address=shipping_address)

            for cart_item in cart.cart_items.all():
                OrderItem.objects.create(
                    order=order, 
                    product=cart_item.product, 
                    qty=cart_item.qty,
                    price_at_purchase=cart_item.product.productPrice)
            
            cart.cart_items.all().delete()

            s_order = OrderSerializer(order)
            return Response({ "message": "Order placed successfully", "data": s_order.data }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
             return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderAdminAPI(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):                             # alternate: id thi get krva mate a 'generics.RetrieveAPIView'use kri nvo class banvo pde lookup_field use krine
        # If 'id' is provided in the URL, retrieve a specific order
        order_id = kwargs.get('id')
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            serializer = self.get_serializer(order)
            return Response(serializer.data)

        # Otherwise, return the full list of orders
        return super().get(request, *args, **kwargs)

class OrderItemAPI(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            order_id = request.query_params.get('id')

            if order_id:
                try:
                    order = Order.objects.get(pk=order_id, user=request.user)
                except Order.DoesNotExist:
                    return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

                order_items = OrderItem.objects.filter(order=order)
            else:
                order_items = OrderItem.objects.filter(order__user = request.user)
            if not order_items.exists():
                return Response({"message": "No Order Items found."}, status=status.HTTP_200_OK)

            s_order_items = OrderItemSerializer(order_items, many=True)
            return Response({"order_items": s_order_items.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)