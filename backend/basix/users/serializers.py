from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, CreatorProfile, InvestorProfile, UserVerification


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'user_type', 'wallet_address', 'profile_image', 'bio',
            'phone_number', 'date_of_birth', 'is_verified', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'wallet_address']


class CreatorProfileSerializer(serializers.ModelSerializer):
    """Creator profile serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CreatorProfile
        fields = [
            'id', 'user', 'skills', 'reputation_score', 'portfolio_url',
            'social_media_links', 'specializations', 'experience_years', 'awards'
        ]
        read_only_fields = ['id']


class InvestorProfileSerializer(serializers.ModelSerializer):
    """Investor profile serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = InvestorProfile
        fields = [
            'id', 'user', 'investment_preferences', 'risk_tolerance',
            'investment_budget', 'preferred_categories', 'investment_history'
        ]
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    # Profile data
    creator_profile = CreatorProfileSerializer(required=False)
    investor_profile = InvestorProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'user_type', 'phone_number',
            'date_of_birth', 'creator_profile', 'investor_profile'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm')
        creator_profile_data = validated_data.pop('creator_profile', None)
        investor_profile_data = validated_data.pop('investor_profile', None)
        
        # Create user
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create appropriate profile based on user type
        if user.user_type == 'creator' and creator_profile_data:
            CreatorProfile.objects.create(user=user, **creator_profile_data)
        elif user.user_type == 'investor' and investor_profile_data:
            InvestorProfile.objects.create(user=user, **investor_profile_data)
        
        # Create verification record
        UserVerification.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Complete user profile serializer"""
    creator_profile = CreatorProfileSerializer(read_only=True)
    investor_profile = InvestorProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'wallet_address', 'profile_image', 'bio',
            'phone_number', 'date_of_birth', 'is_verified',
            'created_at', 'updated_at', 'creator_profile', 'investor_profile'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'wallet_address']


class UserUpdateSerializer(serializers.ModelSerializer):
    """User update serializer"""
    creator_profile = CreatorProfileSerializer(required=False)
    investor_profile = InvestorProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'profile_image', 'bio',
            'phone_number', 'date_of_birth', 'creator_profile', 'investor_profile'
        ]
    
    def update(self, instance, validated_data):
        creator_profile_data = validated_data.pop('creator_profile', None)
        investor_profile_data = validated_data.pop('investor_profile', None)
        
        # Update user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profiles
        if instance.user_type == 'creator' and creator_profile_data:
            creator_profile, created = CreatorProfile.objects.get_or_create(user=instance)
            for attr, value in creator_profile_data.items():
                setattr(creator_profile, attr, value)
            creator_profile.save()
        
        elif instance.user_type == 'investor' and investor_profile_data:
            investor_profile, created = InvestorProfile.objects.get_or_create(user=instance)
            for attr, value in investor_profile_data.items():
                setattr(investor_profile, attr, value)
            investor_profile.save()
        
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """Password change serializer"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value


class EmailVerificationSerializer(serializers.Serializer):
    """Email verification serializer"""
    token = serializers.CharField(required=True)


class PhoneVerificationSerializer(serializers.Serializer):
    """Phone verification serializer"""
    phone_number = serializers.CharField(required=True)
    verification_code = serializers.CharField(required=True)


class TokenResponseSerializer(serializers.Serializer):
    """Token response serializer"""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserProfileSerializer()


class UserStatsSerializer(serializers.Serializer):
    """User statistics serializer"""
    total_products = serializers.IntegerField()
    total_investments = serializers.IntegerField()
    reputation_score = serializers.IntegerField()
    total_earnings = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)