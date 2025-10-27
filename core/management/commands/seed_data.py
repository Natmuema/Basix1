from decimal import Decimal
from django.core.management.base import BaseCommand

from core.models import (
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


class Command(BaseCommand):
    help = "Seed the database with the Marketplace Knowledge Base data"

    def handle(self, *args, **options):
        # Utilities
        utility_codes = [
            "provenance",
            "resale_rights",
            "streaming_rights",
            "royalties",
            "redeem_physical",
            "digital_wearable",
            "redeemable_experience",
            "eco_tourism_support",
            "archive_access",
            "preservation_funding",
            "license_key",
            "subscription_access",
            "royalty_share",
            "lifetime_access",
            "in_game_assets",
            "updates_access",
        ]
        code_to_utility = {}
        for code in utility_codes:
            util, _ = Utility.objects.get_or_create(code=code)
            code_to_utility[code] = util

        # Skills
        skills_map = {}
        for skill_name in ["art", "beadwork", "music", "performance", "fashion", "design", "software", "ai", "games"]:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            skills_map[skill_name] = skill

        # Creators with reputation
        creators_data = [
            {"name": "Alice", "wallet": "addr1", "skills": ["art", "beadwork"], "reputation": 80},
            {"name": "Bob", "wallet": "addr2", "skills": ["music", "performance"], "reputation": 70},
            {"name": "Charlie", "wallet": "addr3", "skills": ["fashion", "design"], "reputation": 65},
            {"name": "David", "wallet": "addr4", "skills": ["software", "ai", "games"], "reputation": 90},
        ]
        name_to_creator = {}
        for c in creators_data:
            creator, _ = Creator.objects.get_or_create(
                name=c["name"], defaults={"wallet_address": c["wallet"], "reputation_score": c["reputation"]}
            )
            # Update fields if needed
            creator.wallet_address = c["wallet"]
            creator.reputation_score = c["reputation"]
            creator.save()
            creator.skills.set([skills_map[s] for s in c["skills"]])
            name_to_creator[c["name"]] = creator

        # Products
        product_specs = [
            {
                "name": "Maasai_Necklace",
                "type": "ArtCraft",
                "description": "Original Maasai Bead Necklace",
                "category": "Beadwork",
                "physical": True,
                "digital": False,
                "digital_scan": True,
                "redeemable": False,
                "license_based": False,
            },
            {
                "name": "AfrobeatTrack1",
                "type": "Music",
                "description": "",
                "category": "Afrobeat",
                "physical": False,
                "digital": True,
                "digital_scan": False,
                "redeemable": False,
                "license_based": False,
            },
            {
                "name": "Maasai_Shuka",
                "type": "Fashion",
                "description": "",
                "category": "Textile",
                "physical": True,
                "digital": False,
                "digital_scan": False,
                "redeemable": True,
                "license_based": False,
            },
            {
                "name": "Safari_Package1",
                "type": "Tourism",
                "description": "3-day Maasai Mara Safari",
                "category": "",
                "physical": False,
                "digital": False,
                "digital_scan": False,
                "redeemable": True,
                "license_based": False,
            },
            {
                "name": "OralHistory1",
                "type": "Heritage",
                "description": "Luo Oral Storytelling Archive",
                "category": "",
                "physical": False,
                "digital": True,
                "digital_scan": False,
                "redeemable": False,
                "license_based": False,
            },
            {
                "name": "AIModel1",
                "type": "Software",
                "description": "AI model for image recognition",
                "category": "AI/ML",
                "physical": False,
                "digital": True,
                "digital_scan": False,
                "redeemable": False,
                "license_based": True,
            },
            {
                "name": "Game1",
                "type": "Software",
                "description": "Indie Game built in Unity",
                "category": "Gaming",
                "physical": False,
                "digital": True,
                "digital_scan": False,
                "redeemable": False,
                "license_based": False,
            },
        ]
        name_to_product = {}
        for spec in product_specs:
            product, _ = Product.objects.get_or_create(name=spec["name"], defaults=spec)
            # Update mutable fields
            for k, v in spec.items():
                setattr(product, k, v)
            product.save()
            name_to_product[spec["name"]] = product

        # NFTs and attach utilities
        nft_specs = [
            {"code": "NFT_MaasaiNecklace", "product": "Maasai_Necklace", "utilities": ["provenance", "resale_rights"]},
            {"code": "NFT_AfrobeatTrack1", "product": "AfrobeatTrack1", "utilities": ["streaming_rights", "royalties"]},
            {"code": "NFT_Shuka1", "product": "Maasai_Shuka", "utilities": ["redeem_physical", "digital_wearable"]},
            {"code": "NFT_Safari1", "product": "Safari_Package1", "utilities": ["redeemable_experience", "eco_tourism_support"]},
            {"code": "NFT_OralHistory1", "product": "OralHistory1", "utilities": ["archive_access", "preservation_funding"]},
            {"code": "NFT_AIModel1", "product": "AIModel1", "utilities": ["license_key", "subscription_access", "royalty_share"]},
            {"code": "NFT_Game1", "product": "Game1", "utilities": ["lifetime_access", "in_game_assets", "updates_access"]},
        ]
        code_to_nft = {}
        for spec in nft_specs:
            nft, _ = NFT.objects.get_or_create(code=spec["code"], defaults={"product": name_to_product[spec["product"]]})
            nft.product = name_to_product[spec["product"]]
            nft.save()
            nft.utilities.set([code_to_utility[c] for c in spec["utilities"]])
            code_to_nft[spec["code"]] = nft

        # Ownerships
        # Use the enhanced ownership where provided
        ownerships = [
            ("NFT_MaasaiNecklace", "Alice", Decimal("70.00")),
            ("NFT_MaasaiNecklace", "Bob", Decimal("30.00")),
            ("NFT_AfrobeatTrack1", "Bob", Decimal("100.00")),
            ("NFT_Shuka1", "Charlie", Decimal("100.00")),
            ("NFT_Safari1", "Alice", Decimal("60.00")),
            ("NFT_Safari1", "Bob", Decimal("40.00")),
            ("NFT_OralHistory1", "Charlie", Decimal("100.00")),
            ("NFT_AIModel1", "David", Decimal("100.00")),
            ("NFT_Game1", "David", Decimal("100.00")),
        ]
        for nft_code, creator_name, pct in ownerships:
            NFTOwnership.objects.update_or_create(
                nft=code_to_nft[nft_code],
                creator=name_to_creator[creator_name],
                defaults={"percentage": pct},
            )

        # Dynamic ownership rules
        DynamicOwnershipRule.objects.update_or_create(
            nft=code_to_nft["NFT_MaasaiNecklace"],
            creator=name_to_creator["Bob"],
            rule_type="transfer_rule",
            defaults={"rule_text": "Bob can gain +10% if he contributes 100 sales"},
        )
        DynamicOwnershipRule.objects.update_or_create(
            nft=code_to_nft["NFT_AfrobeatTrack1"],
            creator=None,
            rule_type="decay_rule",
            defaults={"rule_text": "Ownership reduces by 5% if not maintained with updates"},
        )

        # Governance votes
        GovernanceVote.objects.update_or_create(
            nft=code_to_nft["NFT_Safari1"],
            creator=name_to_creator["Alice"],
            defaults={"weight": Decimal("0.6"), "reputation_weighted": True},
        )
        GovernanceVote.objects.update_or_create(
            nft=code_to_nft["NFT_Safari1"],
            creator=name_to_creator["Bob"],
            defaults={"weight": Decimal("0.4"), "reputation_weighted": True},
        )

        # SDG Tags
        def get_tags(names):
            tags = []
            for n in names:
                tag, _ = SDGTag.objects.get_or_create(name=n)
                tags.append(tag)
            return tags

        # Impact scores
        impacts = [
            ("NFT_Safari1", 90, 85, ["Tourism", "Wildlife_Protection"]),
            ("NFT_OralHistory1", 95, 70, ["Culture", "Education"]),
            ("NFT_AIModel1", 40, 60, ["Innovation", "Tech4Good"]),
            ("NFT_MaasaiNecklace", 85, 80, ["Artisan_Economy", "Women_Empowerment"]),
        ]
        for code, heritage, sustain, tags in impacts:
            impact, _ = ImpactScore.objects.update_or_create(
                nft=code_to_nft[code],
                defaults={"heritage_value": heritage, "sustainability_score": sustain},
            )
            impact.sdg_alignment.set(get_tags(tags))

        # Funding thresholds
        thresholds = [
            ("NFT_MaasaiNecklace", 500),
            ("NFT_AfrobeatTrack1", 1000),
            ("NFT_Shuka1", 700),
            ("NFT_Safari1", 2000),
            ("NFT_OralHistory1", 1500),
            ("NFT_AIModel1", 5000),
            ("NFT_Game1", 3000),
        ]
        for code, amount in thresholds:
            FundingThreshold.objects.update_or_create(
                nft=code_to_nft[code], defaults={"amount": Decimal(str(amount))}
            )

        # Utility gates
        UtilityGate.objects.update_or_create(
            nft=code_to_nft["NFT_Shuka1"],
            utility=code_to_utility["redeem_physical"],
            condition=">=20% ownership required",
        )
        UtilityGate.objects.update_or_create(
            nft=code_to_nft["NFT_AIModel1"],
            utility=code_to_utility["royalty_share"],
            condition=">=50% ownership required",
        )
        UtilityGate.objects.update_or_create(
            nft=code_to_nft["NFT_Game1"],
            utility=code_to_utility["updates_access"],
            condition="subscription_active",
        )

        # History events
        NFTActionHistory.objects.create(nft=code_to_nft["NFT_MaasaiNecklace"], action="sold_to_userX")
        NFTActionHistory.objects.create(nft=code_to_nft["NFT_AfrobeatTrack1"], action="streamed_1000_times")

        self.stdout.write(self.style.SUCCESS("Seed data successfully loaded."))

