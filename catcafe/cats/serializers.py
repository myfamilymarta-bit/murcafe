from . import models
from rest_framework import serializers

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cat
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Staff
        fields = '__all__'

class StaffReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffReview
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactMessage
        fields = '__all__'
