from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Creator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CreatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_verified_creator = serializers.ReadOnlyField()
    total_nfts_created = serializers.ReadOnlyField()
    
    class Meta:
        model = Creator
        fields = [
            'id', 'user', 'wallet_address', 'skills', 'reputation_score',
            'bio', 'profile_image', 'is_verified_creator', 'total_nfts_created',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CreatorCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Creator
        fields = [
            'wallet_address', 'skills', 'bio', 'profile_image',
            'username', 'email', 'password'
        ]
    
    def create(self, validated_data):
        # Extract user data if provided
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        
        # Create user if credentials provided
        user = None
        if username and password:
            user = User.objects.create_user(
                username=username,
                email=email or '',
                password=password
            )
        
        # Create creator
        creator = Creator.objects.create(user=user, **validated_data)
        return creator


class CreatorSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing many creators"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Creator
        fields = ['id', 'username', 'wallet_address', 'reputation_score']