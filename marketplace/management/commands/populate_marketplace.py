from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from marketplace.models import (
    Creator, Product, NFT, Utility, Ownership, DynamicOwnership,
    GovernanceVote, UtilityGate, ImpactScore, FundingThreshold,
    CreatorStats, MarketplaceConfig
)


class Command(BaseCommand):
    help = 'Populate the marketplace database with sample data from the knowledge base'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate marketplace database...')
        
        with transaction.atomic():
            # Create users and creators
            creators_data = [
                {
                    'username': 'alice',
                    'email': 'alice@example.com',
                    'first_name': 'Alice',
                    'last_name': 'Creator',
                    'wallet_address': 'addr1',
                    'skills': ['art', 'beadwork'],
                    'reputation_score': 80
                },
                {
                    'username': 'bob',
                    'email': 'bob@example.com',
                    'first_name': 'Bob',
                    'last_name': 'Musician',
                    'wallet_address': 'addr2',
                    'skills': ['music', 'performance'],
                    'reputation_score': 70
                },
                {
                    'username': 'charlie',
                    'email': 'charlie@example.com',
                    'first_name': 'Charlie',
                    'last_name': 'Designer',
                    'wallet_address': 'addr3',
                    'skills': ['fashion', 'design'],
                    'reputation_score': 65
                },
                {
                    'username': 'david',
                    'email': 'david@example.com',
                    'first_name': 'David',
                    'last_name': 'Developer',
                    'wallet_address': 'addr4',
                    'skills': ['software', 'ai', 'games'],
                    'reputation_score': 90
                }
            ]
            
            creators = []
            for creator_data in creators_data:
                user, created = User.objects.get_or_create(
                    username=creator_data['username'],
                    defaults={
                        'email': creator_data['email'],
                        'first_name': creator_data['first_name'],
                        'last_name': creator_data['last_name']
                    }
                )
                if created:
                    user.set_password('password123')
                    user.save()
                
                creator, created = Creator.objects.get_or_create(
                    user=user,
                    defaults={
                        'wallet_address': creator_data['wallet_address'],
                        'skills': creator_data['skills'],
                        'reputation_score': creator_data['reputation_score']
                    }
                )
                creators.append(creator)
                self.stdout.write(f'Created creator: {creator.user.username}')
            
            # Create products and NFTs
            products_data = [
                {
                    'name': 'Maasai Necklace',
                    'product_type': 'ArtCraft',
                    'category': 'Beadwork',
                    'description': 'Original Maasai Bead Necklace',
                    'is_physical': True,
                    'has_digital_scan': True,
                    'creator': creators[0],  # Alice
                    'price': 500.00,
                    'utilities': ['provenance', 'resale_rights'],
                    'funding_threshold': 500,
                    'impact_score': {
                        'heritage_value': 85,
                        'sustainability_score': 80,
                        'sdg_alignment': ['Artisan_Economy', 'Women_Empowerment']
                    }
                },
                {
                    'name': 'Afrobeat Track 1',
                    'product_type': 'Music',
                    'category': 'Afrobeat',
                    'description': 'Original Afrobeat Music Track',
                    'is_digital': True,
                    'creator': creators[1],  # Bob
                    'price': 1000.00,
                    'utilities': ['streaming_rights', 'royalties'],
                    'funding_threshold': 1000,
                    'impact_score': {
                        'heritage_value': 75,
                        'sustainability_score': 70,
                        'sdg_alignment': ['Culture', 'Music_Preservation']
                    }
                },
                {
                    'name': 'Maasai Shuka',
                    'product_type': 'Fashion',
                    'category': 'Textile',
                    'description': 'Traditional Maasai Shuka',
                    'is_physical': True,
                    'is_redeemable': True,
                    'creator': creators[2],  # Charlie
                    'price': 700.00,
                    'utilities': ['redeem_physical', 'digital_wearable'],
                    'funding_threshold': 700,
                    'impact_score': {
                        'heritage_value': 80,
                        'sustainability_score': 75,
                        'sdg_alignment': ['Traditional_Crafts', 'Cultural_Preservation']
                    }
                },
                {
                    'name': 'Safari Package 1',
                    'product_type': 'Tourism',
                    'category': 'Safari',
                    'description': '3-day Maasai Mara Safari',
                    'is_redeemable': True,
                    'creator': creators[0],  # Alice
                    'price': 2000.00,
                    'utilities': ['redeemable_experience', 'eco_tourism_support'],
                    'funding_threshold': 2000,
                    'impact_score': {
                        'heritage_value': 90,
                        'sustainability_score': 85,
                        'sdg_alignment': ['Tourism', 'Wildlife_Protection']
                    }
                },
                {
                    'name': 'Oral History 1',
                    'product_type': 'Heritage',
                    'category': 'Oral_History',
                    'description': 'Luo Oral Storytelling Archive',
                    'is_digital': True,
                    'creator': creators[2],  # Charlie
                    'price': 1500.00,
                    'utilities': ['archive_access', 'preservation_funding'],
                    'funding_threshold': 1500,
                    'impact_score': {
                        'heritage_value': 95,
                        'sustainability_score': 70,
                        'sdg_alignment': ['Culture', 'Education']
                    }
                },
                {
                    'name': 'AI Model 1',
                    'product_type': 'Software',
                    'category': 'AI/ML',
                    'description': 'AI model for image recognition',
                    'is_digital': True,
                    'is_license_based': True,
                    'creator': creators[3],  # David
                    'price': 5000.00,
                    'utilities': ['license_key', 'subscription_access', 'royalty_share'],
                    'funding_threshold': 5000,
                    'impact_score': {
                        'heritage_value': 40,
                        'sustainability_score': 60,
                        'sdg_alignment': ['Innovation', 'Tech4Good']
                    }
                },
                {
                    'name': 'Game 1',
                    'product_type': 'Software',
                    'category': 'Gaming',
                    'description': 'Indie Game built in Unity',
                    'is_digital': True,
                    'creator': creators[3],  # David
                    'price': 3000.00,
                    'utilities': ['lifetime_access', 'in_game_assets', 'updates_access'],
                    'funding_threshold': 3000,
                    'impact_score': {
                        'heritage_value': 30,
                        'sustainability_score': 50,
                        'sdg_alignment': ['Entertainment', 'Digital_Art']
                    }
                }
            ]
            
            nfts = []
            for product_data in products_data:
                utilities = product_data.pop('utilities')
                funding_threshold = product_data.pop('funding_threshold')
                impact_score_data = product_data.pop('impact_score')
                
                # Create product
                product = Product.objects.create(**product_data)
                
                # Create NFT
                nft = NFT.objects.create(
                    product=product,
                    token_id=f"NFT_{product.name.replace(' ', '')}",
                    blockchain_address=f"0x{product.name.lower().replace(' ', '')}123",
                    contract_address=f"0xcontract{product.name.lower().replace(' ', '')}456"
                )
                nfts.append(nft)
                
                # Create utilities
                for utility_type in utilities:
                    Utility.objects.create(
                        nft=nft,
                        utility_type=utility_type
                    )
                
                # Create funding threshold
                FundingThreshold.objects.create(
                    nft=nft,
                    amount=funding_threshold
                )
                
                # Create impact score
                ImpactScore.objects.create(
                    nft=nft,
                    heritage_value=impact_score_data['heritage_value'],
                    sustainability_score=impact_score_data['sustainability_score'],
                    sdg_alignment=impact_score_data['sdg_alignment']
                )
                
                self.stdout.write(f'Created NFT: {nft.token_id} for {product.name}')
            
            # Create ownership records
            ownership_data = [
                (nfts[0], creators[0], 100.00),  # Alice owns Maasai Necklace 100%
                (nfts[1], creators[1], 100.00),  # Bob owns Afrobeat Track 100%
                (nfts[2], creators[2], 100.00),  # Charlie owns Maasai Shuka 100%
                (nfts[3], creators[0], 60.00),   # Alice owns Safari Package 60%
                (nfts[3], creators[1], 40.00),   # Bob owns Safari Package 40%
                (nfts[4], creators[2], 100.00),  # Charlie owns Oral History 100%
                (nfts[5], creators[3], 100.00),  # David owns AI Model 100%
                (nfts[6], creators[3], 100.00),  # David owns Game 100%
            ]
            
            for nft, creator, percentage in ownership_data:
                Ownership.objects.create(
                    nft=nft,
                    owner=creator,
                    percentage=percentage
                )
            
            # Create dynamic ownership rules
            DynamicOwnership.objects.create(
                nft=nfts[0],
                rule_type='transfer_rule',
                rule_description='Bob can gain +10% if he contributes 100 sales'
            )
            
            DynamicOwnership.objects.create(
                nft=nfts[1],
                rule_type='decay_rule',
                rule_description='Ownership reduces by 5% if not maintained with updates'
            )
            
            # Create governance votes
            GovernanceVote.objects.create(
                nft=nfts[3],  # Safari Package
                voter=creators[0],  # Alice
                weight=0.60,
                is_reputation_weighted=True,
                vote_data={'vote': 'approve', 'reason': 'Eco-tourism initiative'}
            )
            
            GovernanceVote.objects.create(
                nft=nfts[3],  # Safari Package
                voter=creators[1],  # Bob
                weight=0.40,
                is_reputation_weighted=True,
                vote_data={'vote': 'approve', 'reason': 'Wildlife conservation'}
            )
            
            # Create utility gates
            UtilityGate.objects.create(
                nft=nfts[2],  # Maasai Shuka
                utility=Utility.objects.get(nft=nfts[2], utility_type='redeem_physical'),
                condition='>=20% ownership required'
            )
            
            UtilityGate.objects.create(
                nft=nfts[5],  # AI Model
                utility=Utility.objects.get(nft=nfts[5], utility_type='royalty_share'),
                condition='>=50% ownership required'
            )
            
            # Create creator stats
            for creator in creators:
                total_nfts = creator.products.count()
                total_owned = creator.owned_nfts.count()
                CreatorStats.objects.create(
                    creator=creator,
                    total_nfts_created=total_nfts,
                    total_sales=total_nfts * 1000,  # Mock data
                    total_royalties_earned=total_nfts * 100,  # Mock data
                    average_rating=creator.reputation_score / 20,  # Convert to 5-star scale
                    followers_count=creator.reputation_score * 10  # Mock data
                )
            
            # Create marketplace configurations
            configs = [
                {
                    'key': 'marketplace_fees',
                    'value': {'platform_fee': 2.5, 'creator_fee': 5.0},
                    'description': 'Platform and creator fee percentages'
                },
                {
                    'key': 'supported_currencies',
                    'value': ['USD', 'EUR', 'GBP', 'KES'],
                    'description': 'Supported currencies for transactions'
                },
                {
                    'key': 'min_ownership_transfer',
                    'value': 1.0,
                    'description': 'Minimum ownership percentage for transfers'
                },
                {
                    'key': 'max_ownership_percentage',
                    'value': 100.0,
                    'description': 'Maximum ownership percentage per NFT'
                }
            ]
            
            for config_data in configs:
                MarketplaceConfig.objects.create(**config_data)
            
            self.stdout.write(
                self.style.SUCCESS('Successfully populated marketplace database!')
            )
            self.stdout.write(f'Created {len(creators)} creators')
            self.stdout.write(f'Created {len(nfts)} NFTs with products')
            self.stdout.write(f'Created {len(ownership_data)} ownership records')
            self.stdout.write(f'Created {len(configs)} marketplace configurations')