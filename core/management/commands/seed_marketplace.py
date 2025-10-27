from django.core.management.base import BaseCommand

from core.models import (
    Creator,
    Product,
    NFT,
    NFTUtility,
    UtilityGate,
    Ownership,
    DynamicOwnershipRule,
    GovernanceVote,
    ImpactScore,
    FundingThreshold,
)


class Command(BaseCommand):
    help = "Seed the database with the provided marketplace knowledge base"

    def handle(self, *args, **options):
        self.stdout.write("Seeding creators...")
        alice, _ = Creator.objects.get_or_create(
            name="Alice",
            defaults={"wallet": "addr1", "skills": ["art", "beadwork"], "reputation_score": 80},
        )
        bob, _ = Creator.objects.get_or_create(
            name="Bob",
            defaults={"wallet": "addr2", "skills": ["music", "performance"], "reputation_score": 70},
        )
        charlie, _ = Creator.objects.get_or_create(
            name="Charlie",
            defaults={"wallet": "addr3", "skills": ["fashion", "design"], "reputation_score": 65},
        )
        david, _ = Creator.objects.get_or_create(
            name="David",
            defaults={"wallet": "addr4", "skills": ["software", "ai", "games"], "reputation_score": 90},
        )

        self.stdout.write("Seeding products and NFTs...")
        # Art & Crafts
        p_necklace, _ = Product.objects.get_or_create(
            name="Maasai_Necklace",
            defaults={
                "type": "ArtCraft",
                "description": "Original Maasai Bead Necklace",
                "category": "Beadwork",
                "physical": True,
                "digital_scan": True,
            },
        )
        nft_necklace, _ = NFT.objects.get_or_create(code="NFT_MaasaiNecklace", defaults={"product": p_necklace})

        # Music
        p_track, _ = Product.objects.get_or_create(
            name="AfrobeatTrack1",
            defaults={"type": "Music", "category": "Afrobeat", "digital": True},
        )
        nft_track, _ = NFT.objects.get_or_create(code="NFT_AfrobeatTrack1", defaults={"product": p_track})

        # Fashion
        p_shuka, _ = Product.objects.get_or_create(
            name="Maasai_Shuka",
            defaults={"type": "Fashion", "category": "Textile", "physical": True, "redeemable": True},
        )
        nft_shuka, _ = NFT.objects.get_or_create(code="NFT_Shuka1", defaults={"product": p_shuka})

        # Tourism
        p_safari, _ = Product.objects.get_or_create(
            name="Safari_Package1",
            defaults={"type": "Tourism", "description": "3-day Maasai Mara Safari", "redeemable": True},
        )
        nft_safari, _ = NFT.objects.get_or_create(code="NFT_Safari1", defaults={"product": p_safari})

        # Heritage
        p_oral, _ = Product.objects.get_or_create(
            name="OralHistory1",
            defaults={"type": "Heritage", "description": "Luo Oral Storytelling Archive", "digital": True},
        )
        nft_oral, _ = NFT.objects.get_or_create(code="NFT_OralHistory1", defaults={"product": p_oral})

        # Software - AI Model
        p_aimodel, _ = Product.objects.get_or_create(
            name="AIModel1",
            defaults={
                "type": "Software",
                "description": "AI model for image recognition",
                "category": "AI/ML",
                "digital": True,
                "license_based": True,
            },
        )
        nft_aimodel, _ = NFT.objects.get_or_create(code="NFT_AIModel1", defaults={"product": p_aimodel})

        # Software - Game
        p_game, _ = Product.objects.get_or_create(
            name="Game1",
            defaults={
                "type": "Software",
                "description": "Indie Game built in Unity",
                "category": "Gaming",
                "digital": True,
            },
        )
        nft_game, _ = NFT.objects.get_or_create(code="NFT_Game1", defaults={"product": p_game})

        self.stdout.write("Seeding utilities and gates...")
        # Utilities
        NFTUtility.objects.get_or_create(nft=nft_necklace, utility_type="provenance")
        NFTUtility.objects.get_or_create(nft=nft_necklace, utility_type="resale_rights")
        NFTUtility.objects.get_or_create(nft=nft_track, utility_type="streaming_rights")
        NFTUtility.objects.get_or_create(nft=nft_track, utility_type="royalties")
        u_redeem_physical, _ = NFTUtility.objects.get_or_create(nft=nft_shuka, utility_type="redeem_physical")
        NFTUtility.objects.get_or_create(nft=nft_shuka, utility_type="digital_wearable")
        NFTUtility.objects.get_or_create(nft=nft_safari, utility_type="redeemable_experience")
        NFTUtility.objects.get_or_create(nft=nft_safari, utility_type="eco_tourism_support")
        NFTUtility.objects.get_or_create(nft=nft_oral, utility_type="archive_access")
        NFTUtility.objects.get_or_create(nft=nft_oral, utility_type="preservation_funding")
        u_license, _ = NFTUtility.objects.get_or_create(nft=nft_aimodel, utility_type="license_key")
        u_sub, _ = NFTUtility.objects.get_or_create(nft=nft_aimodel, utility_type="subscription_access")
        u_royalty, _ = NFTUtility.objects.get_or_create(nft=nft_aimodel, utility_type="royalty_share")
        NFTUtility.objects.get_or_create(nft=nft_game, utility_type="lifetime_access")
        u_assets, _ = NFTUtility.objects.get_or_create(nft=nft_game, utility_type="in_game_assets")
        u_updates, _ = NFTUtility.objects.get_or_create(nft=nft_game, utility_type="updates_access")

        # Utility gating
        UtilityGate.objects.get_or_create(nft_utility=u_redeem_physical, condition=">=20% ownership required")
        UtilityGate.objects.get_or_create(nft_utility=u_royalty, condition=">=50% ownership required")
        UtilityGate.objects.get_or_create(nft_utility=u_updates, condition="subscription_active")

        self.stdout.write("Seeding ownership and governance...")
        # Ownership examples
        Ownership.objects.update_or_create(nft=nft_necklace, creator=alice, defaults={"percentage": 70})
        Ownership.objects.update_or_create(nft=nft_necklace, creator=bob, defaults={"percentage": 30})

        Ownership.objects.update_or_create(nft=nft_track, creator=bob, defaults={"percentage": 100})
        Ownership.objects.update_or_create(nft=nft_shuka, creator=charlie, defaults={"percentage": 100})
        Ownership.objects.update_or_create(nft=nft_safari, creator=alice, defaults={"percentage": 60})
        Ownership.objects.update_or_create(nft=nft_safari, creator=bob, defaults={"percentage": 40})
        Ownership.objects.update_or_create(nft=nft_oral, creator=charlie, defaults={"percentage": 100})
        Ownership.objects.update_or_create(nft=nft_aimodel, creator=david, defaults={"percentage": 100})
        Ownership.objects.update_or_create(nft=nft_game, creator=david, defaults={"percentage": 100})

        # Dynamic ownership
        DynamicOwnershipRule.objects.get_or_create(
            nft=nft_necklace, rule_type="transfer_rule", description="Bob can gain +10% if he contributes 100 sales"
        )
        DynamicOwnershipRule.objects.get_or_create(
            nft=nft_track, rule_type="decay_rule", description="Ownership reduces by 5% if not maintained with updates"
        )

        # Governance (reputation weighted)
        GovernanceVote.objects.update_or_create(
            nft=nft_safari, creator=alice, defaults={"weight": 0.6, "reputation_weighted": True}
        )
        GovernanceVote.objects.update_or_create(
            nft=nft_safari, creator=bob, defaults={"weight": 0.4, "reputation_weighted": True}
        )

        self.stdout.write("Seeding impact scores and funding thresholds...")
        ImpactScore.objects.update_or_create(
            nft=nft_safari,
            defaults={
                "heritage_value": 90,
                "sustainability_score": 85,
                "sdg_alignment": ["Tourism", "Wildlife_Protection"],
                "computed_value": 88,
            },
        )
        ImpactScore.objects.update_or_create(
            nft=nft_oral,
            defaults={
                "heritage_value": 95,
                "sustainability_score": 70,
                "sdg_alignment": ["Culture", "Education"],
            },
        )
        ImpactScore.objects.update_or_create(
            nft=nft_aimodel,
            defaults={
                "heritage_value": 40,
                "sustainability_score": 60,
                "sdg_alignment": ["Innovation", "Tech4Good"],
            },
        )
        ImpactScore.objects.update_or_create(
            nft=nft_necklace,
            defaults={
                "heritage_value": 85,
                "sustainability_score": 80,
                "sdg_alignment": ["Artisan_Economy", "Women_Empowerment"],
            },
        )

        # Funding thresholds
        FundingThreshold.objects.update_or_create(nft=nft_necklace, defaults={"amount": 500})
        FundingThreshold.objects.update_or_create(nft=nft_track, defaults={"amount": 1000})
        FundingThreshold.objects.update_or_create(nft=nft_shuka, defaults={"amount": 700})
        FundingThreshold.objects.update_or_create(nft=nft_safari, defaults={"amount": 2000})
        FundingThreshold.objects.update_or_create(nft=nft_oral, defaults={"amount": 1500})
        FundingThreshold.objects.update_or_create(nft=nft_aimodel, defaults={"amount": 5000})
        FundingThreshold.objects.update_or_create(nft=nft_game, defaults={"amount": 3000})

        # Smart function examples
        nft_necklace.append_history("sold_to_userX")
        nft_track.append_history("streamed_1000_times")

        self.stdout.write(self.style.SUCCESS("Seeding complete."))

