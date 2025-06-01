from rest_framework import serializers
from .models import User, Property, Booking, Payment, Review, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class PropertySerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    
    class Meta:
        model = Property
        fields = [
            'id', 'host', 'name', 'description', 'location', 
            'price_per_night', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(),
        source='property',
        write_only=True
    )
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'property', 'property_id', 'user', 'start_date', 
            'end_date', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'total_price']

class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'payment_method', 'payment_date']
        read_only_fields = ['id', 'payment_date']

class ReviewSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'property', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'message_body', 'sent_at']
        read_only_fields = ['id', 'sent_at']