from decimal import Decimal

from django.db.models import Sum
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Skill,
    Creator,
    Product,
    Utility,
    NFT,
    NFTOwnership,
    DynamicOwnershipRule,
    GovernanceVote,
    SDGTag,
    ImpactScore,
    FundingThreshold,
    UtilityGate,
    NFTActionHistory,
)
from .serializers import (
    SkillSerializer,
    CreatorSerializer,
    ProductSerializer,
    UtilitySerializer,
    NFTSerializer,
    NFTOwnershipSerializer,
    DynamicOwnershipRuleSerializer,
    GovernanceVoteSerializer,
    SDGTagSerializer,
    ImpactScoreSerializer,
    FundingThresholdSerializer,
    UtilityGateSerializer,
    NFTActionHistorySerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ["id"]


class SkillViewSet(BaseViewSet):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    search_fields = ["name"]


class CreatorViewSet(BaseViewSet):
    queryset = Creator.objects.all().order_by("name")
    serializer_class = CreatorSerializer
    search_fields = ["name", "wallet_address"]


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer
    search_fields = ["name", "type", "category"]


class UtilityViewSet(BaseViewSet):
    queryset = Utility.objects.all().order_by("code")
    serializer_class = UtilitySerializer
    search_fields = ["code"]


class NFTViewSet(BaseViewSet):
    queryset = NFT.objects.all().order_by("code")
    serializer_class = NFTSerializer
    search_fields = ["code", "product__name", "product__type"]

    @action(detail=True, methods=["post"])
    def append_history(self, request, pk=None):
        nft = self.get_object()
        action_text = request.data.get("action")
        if not action_text:
            return Response({"detail": "'action' is required"}, status=status.HTTP_400_BAD_REQUEST)
        event = NFTActionHistory.objects.create(nft=nft, action=action_text)
        return Response(NFTActionHistorySerializer(event).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def impact_score(self, request, pk=None):
        nft = self.get_object()

        # Base: average of heritage and sustainability if defined
        base_score = Decimal("0")
        if hasattr(nft, "impact"):
            base_score = (Decimal(nft.impact.heritage_value) + Decimal(nft.impact.sustainability_score)) / Decimal("2")

        # Votes component: sum(weight * creator_reputation/100) * 100 (normalize to 0..100)
        votes = GovernanceVote.objects.filter(nft=nft).select_related("creator")
        votes_component = Decimal("0")
        for vote in votes:
            reputation_factor = Decimal(vote.creator.reputation_score) / Decimal("100") if vote.reputation_weighted else Decimal("1")
            votes_component += Decimal(vote.weight) * reputation_factor * Decimal("100")

        # Combine with a simple weighted blend: 70% base, 30% votes, clamp 0..100
        final = (base_score * Decimal("0.7")) + (votes_component * Decimal("0.3"))
        final = max(Decimal("0"), min(Decimal("100"), final))

        return Response({"nft": nft.id, "code": nft.code, "impact_score": float(final)})


class NFTOwnershipViewSet(BaseViewSet):
    queryset = NFTOwnership.objects.all().select_related("nft", "creator")
    serializer_class = NFTOwnershipSerializer
    search_fields = ["nft__code", "creator__name"]


class DynamicOwnershipRuleViewSet(BaseViewSet):
    queryset = DynamicOwnershipRule.objects.all()
    serializer_class = DynamicOwnershipRuleSerializer
    search_fields = ["nft__code", "creator__name", "rule_text", "rule_type"]


class GovernanceVoteViewSet(BaseViewSet):
    queryset = GovernanceVote.objects.all().select_related("nft", "creator")
    serializer_class = GovernanceVoteSerializer
    search_fields = ["nft__code", "creator__name"]


class SDGTagViewSet(BaseViewSet):
    queryset = SDGTag.objects.all().order_by("name")
    serializer_class = SDGTagSerializer
    search_fields = ["name"]


class ImpactScoreViewSet(BaseViewSet):
    queryset = ImpactScore.objects.all().select_related("nft")
    serializer_class = ImpactScoreSerializer
    search_fields = ["nft__code"]


class FundingThresholdViewSet(BaseViewSet):
    queryset = FundingThreshold.objects.all().select_related("nft")
    serializer_class = FundingThresholdSerializer
    search_fields = ["nft__code"]


class UtilityGateViewSet(BaseViewSet):
    queryset = UtilityGate.objects.all().select_related("nft", "utility")
    serializer_class = UtilityGateSerializer
    search_fields = ["nft__code", "utility__code", "condition"]


class NFTActionHistoryViewSet(BaseViewSet):
    queryset = NFTActionHistory.objects.all().select_related("nft")
    serializer_class = NFTActionHistorySerializer
    search_fields = ["nft__code", "action"]

from django.shortcuts import render

# Create your views here.
