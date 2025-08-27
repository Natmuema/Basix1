from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Transaction, ImpactMetrics, MarketplaceStats
from .serializers import (
    TransactionSerializer, TransactionCreateSerializer,
    ImpactMetricsSerializer, MarketplaceStatsSerializer
)
from .utils import (
    generate_marketplace_stats, calculate_impact_score,
    get_accessible_utilities
)
from nfts.models import NFT
from creators.models import Creator


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing transactions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Transaction.objects.all()
        
        # Filter by transaction type
        transaction_type = self.request.query_params.get('type', None)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by NFT
        nft_id = self.request.query_params.get('nft_id', None)
        if nft_id:
            queryset = queryset.filter(nft_id=nft_id)
        
        # Filter by creator
        creator_id = self.request.query_params.get('creator_id', None)
        if creator_id:
            queryset = queryset.filter(
                Q(from_creator_id=creator_id) | Q(to_creator_id=creator_id)
            )
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        
        # Update NFT history
        transaction.nft.append_history(
            f'transaction_{transaction.transaction_type}',
            {
                'transaction_id': transaction.id,
                'amount': float(transaction.amount) if transaction.amount else None,
                'from': transaction.from_creator.id if transaction.from_creator else None,
                'to': transaction.to_creator.id if transaction.to_creator else None
            }
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            TransactionSerializer(transaction).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ImpactMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing impact metrics.
    """
    queryset = ImpactMetrics.objects.all()
    serializer_class = ImpactMetricsSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = ImpactMetrics.objects.all()
        
        # Filter by NFT
        nft_id = self.request.query_params.get('nft_id', None)
        if nft_id:
            queryset = queryset.filter(nft_id=nft_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(recorded_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(recorded_at__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def latest_by_nft(self, request):
        """Get latest metrics for each NFT"""
        nft_id = request.query_params.get('nft_id', None)
        
        if nft_id:
            metric = ImpactMetrics.objects.filter(
                nft_id=nft_id
            ).order_by('-recorded_at').first()
            
            if metric:
                serializer = self.get_serializer(metric)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'No metrics found for this NFT'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Get latest metric for each NFT
        from django.db.models import Max
        latest_metrics = []
        
        # Get distinct NFT IDs with their latest metric date
        latest_dates = ImpactMetrics.objects.values('nft').annotate(
            latest=Max('recorded_at')
        )
        
        for item in latest_dates:
            metric = ImpactMetrics.objects.get(
                nft_id=item['nft'],
                recorded_at=item['latest']
            )
            latest_metrics.append(metric)
        
        serializer = self.get_serializer(latest_metrics, many=True)
        return Response(serializer.data)


class MarketplaceStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing marketplace statistics.
    """
    queryset = MarketplaceStats.objects.all()
    serializer_class = MarketplaceStatsSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = MarketplaceStats.objects.all()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current day statistics"""
        today = timezone.now().date()
        stats = MarketplaceStats.objects.filter(date=today).first()
        
        if not stats:
            # Generate stats if not exists
            stats = generate_marketplace_stats(today)
        
        serializer = self.get_serializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate statistics for a specific date"""
        date_str = request.data.get('date', None)
        
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            date = timezone.now().date()
        
        stats = generate_marketplace_stats(date)
        serializer = self.get_serializer(stats)
        return Response(serializer.data)


@api_view(['POST'])
def calculate_nft_impact_score(request):
    """
    Calculate impact score for a specific NFT.
    """
    nft_id = request.data.get('nft_id')
    
    if not nft_id:
        return Response(
            {'error': 'nft_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    nft = get_object_or_404(NFT, pk=nft_id)
    impact_score = calculate_impact_score(nft)
    
    # Get average creator reputation
    creator_reputations = [
        ownership.creator.reputation_score 
        for ownership in nft.ownerships.all()
    ]
    avg_reputation = sum(creator_reputations) / len(creator_reputations) if creator_reputations else 50
    
    return Response({
        'nft_id': nft_id,
        'impact_score': impact_score,
        'heritage_value': nft.heritage_value,
        'sustainability_score': nft.sustainability_score,
        'creator_reputation_avg': avg_reputation
    })


@api_view(['GET'])
def check_utility_access(request):
    """
    Check which utilities a creator can access for an NFT.
    """
    creator_id = request.query_params.get('creator_id')
    nft_id = request.query_params.get('nft_id')
    
    if not creator_id or not nft_id:
        return Response(
            {'error': 'Both creator_id and nft_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    creator = get_object_or_404(Creator, pk=creator_id)
    nft = get_object_or_404(NFT, pk=nft_id)
    
    # Get ownership percentage
    try:
        ownership = nft.ownerships.get(creator=creator)
        ownership_percentage = float(ownership.percentage)
    except:
        ownership_percentage = 0
    
    # Get accessible utilities
    accessible_utilities = get_accessible_utilities(nft, creator)
    
    from nfts.serializers import UtilitySerializer
    
    return Response({
        'creator_id': creator_id,
        'nft_id': nft_id,
        'ownership_percentage': ownership_percentage,
        'accessible_utilities': UtilitySerializer(accessible_utilities, many=True).data,
        'total_utilities': nft.utilities.count()
    })