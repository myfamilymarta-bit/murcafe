from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from . import serializers
from . import models


class CatListApiView(ListAPIView):
    serializer_class = serializers.CatSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['gender', 'age', 'status', 'temperament']

    def get_queryset(self):
        return models.Cat.objects.all()



class MenuItemListApiView(ListAPIView):
    serializer_class = serializers.MenuItemSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['category', 'vegetarian', 'is_available']
    ordering_fields = ['price', 'name']

    def get_queryset(self):
        return models.MenuItem.objects.all()



class StaffListApiView(ListAPIView):
    serializer_class = serializers.StaffSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['position', 'is_active']
    ordering_fields = ['first_name', 'last_name']

    def get_queryset(self):
        return models.Staff.objects.all()



class StaffReviewListApiView(ListAPIView):
    serializer_class = serializers.StaffReviewSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['staff', 'rating', 'is_approved']
    ordering_fields = ['created_at', 'rating']

    def get_queryset(self):
        return models.StaffReview.objects.all()


class ContactMessageListApiView(ListAPIView):
    serializer_class = serializers.ContactMessageSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ['created_at']

    def get_queryset(self):
        return models.ContactMessage.objects.all()
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from . import serializers
from . import models


class CatListApiView(ListAPIView):
    serializer_class = serializers.CatSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['gender', 'age', 'status', 'temperament']

    def get_queryset(self):
        return models.Cat.objects.all()



class MenuItemListApiView(ListAPIView):
    serializer_class = serializers.MenuItemSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['category', 'vegetarian', 'is_available']
    ordering_fields = ['price', 'name']

    def get_queryset(self):
        return models.MenuItem.objects.all()



class StaffListApiView(ListAPIView):
    serializer_class = serializers.StaffSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['position', 'is_active']
    ordering_fields = ['first_name', 'last_name']

    def get_queryset(self):
        return models.Staff.objects.all()



class StaffReviewListApiView(ListAPIView):
    serializer_class = serializers.StaffReviewSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['staff', 'rating', 'is_approved']
    ordering_fields = ['created_at', 'rating']

    def get_queryset(self):
        return models.StaffReview.objects.all()


class ContactMessageListApiView(ListAPIView):
    serializer_class = serializers.ContactMessageSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ['created_at']

    def get_queryset(self):
        return models.ContactMessage.objects.all()
