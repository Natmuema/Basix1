from django.db.models import Avg, F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Creator,
    Product,
    NFT,
    NFTEvent,
    NFTUtility,
    UtilityGate,
    Ownership,
    DynamicOwnershipRule,
    GovernanceVote,
    ImpactScore,
    FundingThreshold,
)
from .serializers import (
    CreatorSerializer,
    ProductSerializer,
    NFTSerializer,
    NFTEventSerializer,
    NFTUtilitySerializer,
    UtilityGateSerializer,
    OwnershipSerializer,
    DynamicOwnershipRuleSerializer,
    GovernanceVoteSerializer,
    ImpactScoreSerializer,
    FundingThresholdSerializer,
)


class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    search_fields = ["name", "wallet", "skills"]
    filterset_fields = ["reputation_score"]
    ordering_fields = ["name", "reputation_score", "id"]

    @action(detail=True, methods=["get"], url_path="is_creator")
    def is_creator(self, request, pk=None):
        creator = self.get_object()
        return Response({"is_creator": creator.is_creator})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ["name", "type", "category", "description"]
    filterset_fields = ["type", "category", "physical", "digital", "redeemable"]
    ordering_fields = ["name", "type", "id"]


class NFTViewSet(viewsets.ModelViewSet):
    queryset = NFT.objects.all().select_related("product")
    serializer_class = NFTSerializer
    search_fields = ["code", "product__name", "product__type", "product__category"]
    filterset_fields = ["product__type", "product__category"]
    ordering_fields = ["code", "id"]

    @action(detail=True, methods=["post"], url_path="append_history")
    def append_history(self, request, pk=None):
        nft = self.get_object()
        action_text = request.data.get("action")
        if not action_text:
            return Response({"detail": "Missing 'action'"}, status=status.HTTP_400_BAD_REQUEST)
        event = nft.append_history(action_text)
        return Response(NFTEventSerializer(event).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="impact_score")
    def impact_score(self, request, pk=None):
        nft = self.get_object()
        impact, _ = ImpactScore.objects.get_or_create(nft=nft)
        if impact.computed_value is not None:
            return Response({"impact_score": impact.computed_value})

        votes = GovernanceVote.objects.filter(nft=nft)
        if votes.exists():
            total_weight = sum(v.weight for v in votes)
            if total_weight > 0:
                weighted_rep = sum((v.creator.reputation_score * v.weight) for v in votes) / total_weight
            else:
                weighted_rep = 0
        else:
            owners = Ownership.objects.filter(nft=nft)
            if owners.exists():
                weighted_rep = sum(o.creator.reputation_score * float(o.percentage) for o in owners) / sum(
                    float(o.percentage) for o in owners
                )
            else:
                weighted_rep = 0

        heritage_value = impact.heritage_value or 0
        sustainability_score = impact.sustainability_score or 0
        computed = int(round(0.5 * weighted_rep + 0.25 * heritage_value + 0.25 * sustainability_score))
        impact.computed_value = computed
        impact.save(update_fields=["computed_value"])
        return Response({"impact_score": computed})


class NFTEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NFTEvent.objects.all().select_related("nft")
    serializer_class = NFTEventSerializer
    filterset_fields = ["nft"]
    ordering_fields = ["created_at", "id"]


class NFTUtilityViewSet(viewsets.ModelViewSet):
    queryset = NFTUtility.objects.all().select_related("nft")
    serializer_class = NFTUtilitySerializer
    filterset_fields = ["nft", "utility_type"]
    ordering_fields = ["utility_type", "id"]


class UtilityGateViewSet(viewsets.ModelViewSet):
    queryset = UtilityGate.objects.all().select_related("nft_utility", "nft_utility__nft")
    serializer_class = UtilityGateSerializer
    filterset_fields = ["nft_utility__nft", "nft_utility__utility_type"]


class OwnershipViewSet(viewsets.ModelViewSet):
    queryset = Ownership.objects.all().select_related("nft", "creator")
    serializer_class = OwnershipSerializer
    filterset_fields = ["nft", "creator"]
    ordering_fields = ["percentage", "id"]


class DynamicOwnershipRuleViewSet(viewsets.ModelViewSet):
    queryset = DynamicOwnershipRule.objects.all().select_related("nft")
    serializer_class = DynamicOwnershipRuleSerializer
    filterset_fields = ["nft", "rule_type"]


class GovernanceVoteViewSet(viewsets.ModelViewSet):
    queryset = GovernanceVote.objects.all().select_related("nft", "creator")
    serializer_class = GovernanceVoteSerializer
    filterset_fields = ["nft", "creator", "reputation_weighted"]


class ImpactScoreViewSet(viewsets.ModelViewSet):
    queryset = ImpactScore.objects.all().select_related("nft")
    serializer_class = ImpactScoreSerializer
    filterset_fields = ["nft"]


class FundingThresholdViewSet(viewsets.ModelViewSet):
    queryset = FundingThreshold.objects.all().select_related("nft")
    serializer_class = FundingThresholdSerializer
    filterset_fields = ["nft"]

from django.shortcuts import render

# Create your views here.
