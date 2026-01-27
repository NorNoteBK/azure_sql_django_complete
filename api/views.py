from rest_framework import generics, response, status
from .models import Store, Product, Order, OrderItem
from .serializers import StoreSerializer, ProductSerializer, UserSerializer, OrderSerializer
from django.contrib.auth.models import User

# Create your views here.


class StoreList(generics.ListCreateAPIView):
    # API view to retrieve list of stores or create a new store
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update or delete a store instance
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'store_id'


class StoreDeleteAll(generics.DestroyAPIView):
    # API view to delete all stores
    def delete(self, request, *args, **kwargs):
        # Delete all Store objects
        Store.objects.all().delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(generics.ListCreateAPIView):
    # API view to retrieve list of products or create a new product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update or delete a product instance
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class UserList(generics.ListCreateAPIView):
    # API view to list and create users
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderList(generics.ListCreateAPIView):
    # API view to list and create orders
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Associate the order with the current user or a default user
        # For simplicity in this demo, we'll assign to the first user if no auth
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        serializer.save(user=user)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update, and delete orders
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductDeleteAll(generics.DestroyAPIView):
    # API view to delete all products
    def delete(self, request, *args, **kwargs):
        Product.objects.all().delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)



class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update or delete a user instance
    queryset = User.objects.all()
    serializer_class = UserSerializer


from rest_framework.views import APIView
from .mongo_utils import get_db_handle
from datetime import datetime
from bson import ObjectId

class ReviewList(APIView):
    # API view to manage Reviews using MongoDB
    
    def get(self, request):
        # List all reviews or filter by product_id
        db = get_db_handle()
        collection = db['reviews']
        
        product_id = request.query_params.get('product_id')
        filter_query = {}
        if product_id:
            filter_query['product_id'] = int(product_id)
        
        # Convert ObjectId to string for JSON serialization
        reviews = list(collection.find(filter_query))
        for review in reviews:
            review['_id'] = str(review['_id'])
            
        return response.Response(reviews)

    def post(self, request):
        # Create a new review
        db = get_db_handle()
        collection = db['reviews']
        
        data = request.data
        review = {
            'product_id': data.get('product_id'),
            'user_id': data.get('user_id'),
            'rating': data.get('rating'),
            'comment': data.get('comment'),
            'created_at': datetime.now().isoformat()
        }
        
        result = collection.insert_one(review)
        review['_id'] = str(result.inserted_id)
        
        return response.Response(review, status=status.HTTP_201_CREATED)


class ReviewDetail(APIView):
    # API view to retrieve, update or delete a specific review from MongoDB
    
    def get_object(self, pk):
        db = get_db_handle()
        collection = db['reviews']
        try:
            return collection.find_one({'_id': ObjectId(pk)})
        except:
            return None

    def get(self, request, pk):
        review = self.get_object(pk)
        if review:
            review['_id'] = str(review['_id'])
            return response.Response(review)
        return response.Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        db = get_db_handle()
        collection = db['reviews']
        
        existing_review = self.get_object(pk)
        if not existing_review:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        update_data = {k: v for k, v in data.items() if k in ['rating', 'comment', 'product_id', 'user_id']}
        update_data['updated_at'] = datetime.now().isoformat()
        
        collection.update_one({'_id': ObjectId(pk)}, {'$set': update_data})
        
        updated_review = collection.find_one({'_id': ObjectId(pk)})
        updated_review['_id'] = str(updated_review['_id'])
        
        return response.Response(updated_review)

    def delete(self, request, pk):
        db = get_db_handle()
        collection = db['reviews']
        
        result = collection.delete_one({'_id': ObjectId(pk)})
        if result.deleted_count > 0:
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(status=status.HTTP_404_NOT_FOUND)


from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return response.Response({
        'stores': reverse('store-list', request=request, format=format),
        'products': reverse('product-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'reviews': reverse('review-list', request=request, format=format),
    })

