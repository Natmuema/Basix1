from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from creators.models import Creator
from products.models import Product
from nfts.models import NFT, Ownership, Utility, GovernanceVote
from utilities.models import Transaction
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load sample data based on the knowledge base'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create users and creators
        creators_data = [
            {'username': 'alice', 'wallet': 'addr1', 'skills': ['art', 'beadwork'], 'reputation': 80},
            {'username': 'bob', 'wallet': 'addr2', 'skills': ['music', 'performance'], 'reputation': 70},
            {'username': 'charlie', 'wallet': 'addr3', 'skills': ['fashion', 'design'], 'reputation': 65},
            {'username': 'david', 'wallet': 'addr4', 'skills': ['software', 'ai', 'games'], 'reputation': 90},
        ]
        
        creators = {}
        for data in creators_data:
            user, _ = User.objects.get_or_create(
                username=data['username'],
                defaults={'email': f"{data['username']}@example.com"}
            )
            creator, _ = Creator.objects.get_or_create(
                user=user,
                defaults={
                    'wallet_address': data['wallet'],
                    'skills': data['skills'],
                    'reputation_score': data['reputation']
                }
            )
            creators[data['username']] = creator
            self.stdout.write(f"Created creator: {data['username']}")
        
        # Create products
        products_data = [
            {
                'name': 'Maasai_Necklace',
                'type': 'ArtCraft',
                'description': 'Original Maasai Bead Necklace',
                'category': 'Beadwork',
                'is_physical': True,
                'is_digital': False,
                'has_digital_scan': True
            },
            {
                'name': 'AfrobeatTrack1',
                'type': 'Music',
                'description': 'Original Afrobeat Track',
                'category': 'Afrobeat',
                'is_physical': False,
                'is_digital': True
            },
            {
                'name': 'Maasai_Shuka',
                'type': 'Fashion',
                'description': 'Traditional Maasai Shuka Textile',
                'category': 'Textile',
                'is_physical': True,
                'is_digital': False,
                'is_redeemable': True
            },
            {
                'name': 'Safari_Package1',
                'type': 'Tourism',
                'description': '3-day Maasai Mara Safari',
                'category': 'Other',
                'is_physical': False,
                'is_digital': False,
                'is_redeemable': True
            },
            {
                'name': 'OralHistory1',
                'type': 'Heritage',
                'description': 'Luo Oral Storytelling Archive',
                'category': 'Other',
                'is_physical': False,
                'is_digital': True
            },
            {
                'name': 'AIModel1',
                'type': 'Software',
                'description': 'AI model for image recognition',
                'category': 'AI/ML',
                'is_physical': False,
                'is_digital': True,
                'is_license_based': True
            },
            {
                'name': 'Game1',
                'type': 'Software',
                'description': 'Indie Game built in Unity',
                'category': 'Gaming',
                'is_physical': False,
                'is_digital': True
            }
        ]
        
        products = {}
        for data in products_data:
            product, _ = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'product_type': data['type'],
                    'description': data['description'],
                    'category': data['category'],
                    'is_physical': data.get('is_physical', False),
                    'is_digital': data.get('is_digital', True),
                    'has_digital_scan': data.get('has_digital_scan', False),
                    'is_redeemable': data.get('is_redeemable', False),
                    'is_license_based': data.get('is_license_based', False)
                }
            )
            products[data['name']] = product
            self.stdout.write(f"Created product: {data['name']}")
        
        # Create NFTs with utilities and ownership
        nfts_data = [
            {
                'token_id': 'NFT_MaasaiNecklace',
                'name': 'NFT Maasai Necklace',
                'product': 'Maasai_Necklace',
                'funding_threshold': 500,
                'heritage_value': 85,
                'sustainability_score': 80,
                'sdg_alignment': ['Artisan_Economy', 'Women_Empowerment'],
                'utilities': ['provenance', 'resale_rights'],
                'ownership': [('alice', 70), ('bob', 30)]
            },
            {
                'token_id': 'NFT_AfrobeatTrack1',
                'name': 'NFT Afrobeat Track 1',
                'product': 'AfrobeatTrack1',
                'funding_threshold': 1000,
                'heritage_value': 70,
                'sustainability_score': 60,
                'sdg_alignment': ['Culture', 'Creative_Economy'],
                'utilities': ['streaming_rights', 'royalties'],
                'ownership': [('bob', 100)]
            },
            {
                'token_id': 'NFT_Shuka1',
                'name': 'NFT Maasai Shuka',
                'product': 'Maasai_Shuka',
                'funding_threshold': 700,
                'heritage_value': 90,
                'sustainability_score': 85,
                'sdg_alignment': ['Fashion', 'Heritage'],
                'utilities': ['redeem_physical', 'digital_wearable'],
                'ownership': [('charlie', 100)]
            },
            {
                'token_id': 'NFT_Safari1',
                'name': 'NFT Safari Package',
                'product': 'Safari_Package1',
                'funding_threshold': 2000,
                'heritage_value': 90,
                'sustainability_score': 85,
                'sdg_alignment': ['Tourism', 'Wildlife_Protection'],
                'utilities': ['redeemable_experience', 'eco_tourism_support'],
                'ownership': [('alice', 60), ('bob', 40)],
                'governance': [('alice', 0.6, True), ('bob', 0.4, True)]
            },
            {
                'token_id': 'NFT_OralHistory1',
                'name': 'NFT Oral History Archive',
                'product': 'OralHistory1',
                'funding_threshold': 1500,
                'heritage_value': 95,
                'sustainability_score': 70,
                'sdg_alignment': ['Culture', 'Education'],
                'utilities': ['archive_access', 'preservation_funding'],
                'ownership': [('charlie', 100)]
            },
            {
                'token_id': 'NFT_AIModel1',
                'name': 'NFT AI Model',
                'product': 'AIModel1',
                'funding_threshold': 5000,
                'heritage_value': 40,
                'sustainability_score': 60,
                'sdg_alignment': ['Innovation', 'Tech4Good'],
                'utilities': ['license_key', 'subscription_access', 'royalty_share'],
                'ownership': [('david', 100)]
            },
            {
                'token_id': 'NFT_Game1',
                'name': 'NFT Indie Game',
                'product': 'Game1',
                'funding_threshold': 3000,
                'heritage_value': 50,
                'sustainability_score': 55,
                'sdg_alignment': ['Entertainment', 'Digital_Content'],
                'utilities': ['lifetime_access', 'in_game_assets', 'updates_access'],
                'ownership': [('david', 100)]
            }
        ]
        
        for nft_data in nfts_data:
            nft, created = NFT.objects.get_or_create(
                token_id=nft_data['token_id'],
                defaults={
                    'name': nft_data['name'],
                    'product': products[nft_data['product']],
                    'funding_threshold': nft_data['funding_threshold'],
                    'heritage_value': nft_data['heritage_value'],
                    'sustainability_score': nft_data['sustainability_score'],
                    'sdg_alignment': nft_data['sdg_alignment']
                }
            )
            
            if created:
                self.stdout.write(f"Created NFT: {nft_data['name']}")
                
                # Create utilities
                for utility_type in nft_data['utilities']:
                    Utility.objects.create(nft=nft, utility_type=utility_type)
                
                # Create ownership
                for creator_name, percentage in nft_data['ownership']:
                    Ownership.objects.create(
                        nft=nft,
                        creator=creators[creator_name],
                        percentage=Decimal(str(percentage))
                    )
                
                # Create governance votes if specified
                if 'governance' in nft_data:
                    for creator_name, weight, rep_weighted in nft_data['governance']:
                        GovernanceVote.objects.create(
                            nft=nft,
                            creator=creators[creator_name],
                            weight=Decimal(str(weight)),
                            is_reputation_weighted=rep_weighted
                        )
                
                # Add initial history
                nft.append_history('nft_minted', {'creator': nft_data['ownership'][0][0]})
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data!'))