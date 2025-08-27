from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum, Count
from django.core.mail import send_mail
from django.conf import settings
import random
import string

from .models import User, CreatorProfile, InvestorProfile, UserVerification, UserSession
from .serializers import (
    UserSerializer, UserProfileSerializer, UserRegistrationSerializer,
    UserLoginSerializer, UserUpdateSerializer, PasswordChangeSerializer,
    EmailVerificationSerializer, PhoneVerificationSerializer,
    TokenResponseSerializer, UserStatsSerializer,
    CreatorProfileSerializer, InvestorProfileSerializer
)


class AuthViewSet(viewsets.ViewSet):
    """Authentication endpoints"""
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    
                    # Generate tokens
                    refresh = RefreshToken.for_user(user)
                    
                    # Create verification record if not exists
                    UserVerification.objects.get_or_create(user=user)
                    
                    return Response({
                        'message': 'User registered successfully',
                        'tokens': {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                        },
                        'user': UserProfileSerializer(user).data
                    }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Login user"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            # Track session
            self._track_session(user, request)
            
            return Response({
                'message': 'Login successful',
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'user': UserProfileSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """Logout user"""
        try:
            # Blacklist refresh token
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Deactivate sessions
            UserSession.objects.filter(
                user=request.user,
                session_key=request.session.session_key
            ).update(is_active=False)
            
            logout(request)
            return Response({'message': 'Logout successful'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """Update user profile"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': UserProfileSerializer(request.user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def send_email_verification(self, request):
        """Send email verification"""
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            verification, created = UserVerification.objects.get_or_create(user=user)
            
            # Generate verification token
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            verification.email_verification_token = token
            verification.email_verification_sent_at = timezone.now()
            verification.save()
            
            # Send email (in production, use proper email service)
            # send_mail(
            #     'Email Verification',
            #     f'Your verification token: {token}',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [email],
            #     fail_silently=False,
            # )
            
            return Response({'message': 'Verification email sent'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def verify_email(self, request):
        """Verify email with token"""
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            try:
                verification = UserVerification.objects.get(email_verification_token=token)
                verification.email_verified = True
                verification.email_verification_token = ''
                verification.save()
                
                user = verification.user
                user.is_verified = True
                user.save()
                
                return Response({'message': 'Email verified successfully'})
            except UserVerification.DoesNotExist:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def send_phone_verification(self, request):
        """Send phone verification code"""
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(phone_number=phone_number)
            verification, created = UserVerification.objects.get_or_create(user=user)
            
            # Generate verification code
            code = ''.join(random.choices(string.digits, k=6))
            verification.phone_verification_code = code
            verification.phone_verification_sent_at = timezone.now()
            verification.save()
            
            # Send SMS (in production, use proper SMS service)
            # This is a mock implementation
            print(f"SMS verification code for {phone_number}: {code}")
            
            return Response({'message': 'Verification code sent'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def verify_phone(self, request):
        """Verify phone with code"""
        serializer = PhoneVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['verification_code']
            
            try:
                user = User.objects.get(phone_number=phone_number)
                verification = user.verification
                
                if verification.phone_verification_code == code:
                    verification.phone_verified = True
                    verification.phone_verification_code = ''
                    verification.save()
                    
                    user.is_verified = True
                    user.save()
                    
                    return Response({'message': 'Phone verified successfully'})
                else:
                    return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def stats(self, request):
        """Get user statistics"""
        user = request.user
        
        # Mock statistics (in real app, calculate from actual data)
        stats = {
            'total_products': 0,
            'total_investments': 0,
            'reputation_score': 0,
            'total_earnings': 0,
            'total_spent': 0,
        }
        
        if user.user_type == 'creator':
            try:
                creator_profile = user.creator_profile
                stats['reputation_score'] = creator_profile.reputation_score
            except CreatorProfile.DoesNotExist:
                pass
        
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)
    
    def _track_session(self, user, request):
        """Track user session"""
        session_key = request.session.session_key
        if session_key:
            UserSession.objects.update_or_create(
                session_key=session_key,
                defaults={
                    'user': user,
                    'ip_address': self._get_client_ip(request),
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'is_active': True,
                }
            )
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserViewSet(viewsets.ModelViewSet):
    """User management viewset"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'me']:
            return UserProfileSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def creators(self, request):
        """Get all creators"""
        creators = User.objects.filter(user_type='creator')
        serializer = UserProfileSerializer(creators, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def investors(self, request):
        """Get all investors"""
        investors = User.objects.filter(user_type='investor')
        serializer = UserProfileSerializer(investors, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get detailed user profile"""
        user = self.get_object()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class CreatorProfileViewSet(viewsets.ModelViewSet):
    """Creator profile management"""
    queryset = CreatorProfile.objects.all()
    serializer_class = CreatorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def top_creators(self, request):
        """Get top creators by reputation"""
        creators = CreatorProfile.objects.order_by('-reputation_score')[:10]
        serializer = CreatorProfileSerializer(creators, many=True)
        return Response(serializer.data)


class InvestorProfileViewSet(viewsets.ModelViewSet):
    """Investor profile management"""
    queryset = InvestorProfile.objects.all()
    serializer_class = InvestorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def top_investors(self, request):
        """Get top investors by budget"""
        investors = InvestorProfile.objects.order_by('-investment_budget')[:10]
        serializer = InvestorProfileSerializer(investors, many=True)
        return Response(serializer.data)
