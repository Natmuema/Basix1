from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from marketplace.models import (
    Creator, Product, NFT, Utility, Ownership, DynamicOwnership,
    GovernanceVote, UtilityGate, ImpactScore, FundingThreshold
)


class Command(BaseCommand):
    help = 'Load marketplace knowledge base data into the database'

    def handle(self, *args, **options):
        self.stdout.write('Loading marketplace knowledge base data...')
        
        # Create users and creators
        creators_data = [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'wallet_address': 'addr1',
                'skills': ['art', 'beadwork'],
                'reputation_score': 80
            },
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'wallet_address': 'addr2',
                'skills': ['music', 'performance'],
                'reputation_score': 70
            },
            {
                'username': 'charlie',
                'email': 'charlie@example.com',
                'wallet_address': 'addr3',
                'skills': ['fashion', 'design'],
                'reputation_score': 65
            },
            {
                'username': 'david',
                'email': 'david@example.com',
                'wallet_address': 'addr4',
                'skills': ['software', 'ai', 'games'],
                'reputation_score': 90
            }
        ]
        
        creators = {}
        for creator_data in creators_data:
            user, created = User.objects.get_or_create(
                username=creator_data['username'],
                defaults={
                    'email': creator_data['email'],
                    'first_name': creator_data['username'].title(),
                    'last_name': 'Creator'
                }
            )
            
            creator, created = Creator.objects.get_or_create(
                user=user,
                defaults={
                    'wallet_address': creator_data['wallet_address'],
                    'skills': creator_data['skills'],
                    'reputation_score': creator_data['reputation_score']
                }
            )
            creators[creator_data['username']] = creator
            
            if created:
                self.stdout.write(f'Created creator: {creator.user.username}')
        
        # Create products
        products_data = [
            {
                'name': 'Maasai_Necklace',
                'product_type': 'ArtCraft',
                'category': 'Beadwork',
                'description': 'Original Maasai Bead Necklace',
                'is_physical': True,
                'has_digital_scan': True,
                'creator': 'alice'
            },
            {
                'name': 'AfrobeatTrack1',
                'product_type': 'Music',
                'category': 'Afrobeat',
                'description': 'Original Afrobeat Music Track',
                'is_digital': True,
                'creator': 'bob'
            },
            {
                'name': 'Maasai_Shuka',
                'product_type': 'Fashion',
                'category': 'Textile',
                'description': 'Traditional Maasai Shuka',
                'is_physical': True,
                'is_redeemable': True,
                'creator': 'charlie'
            },
            {
                'name': 'Safari_Package1',
                'product_type': 'Tourism',
                'description': '3-day Maasai Mara Safari',
                'is_redeemable': True,
                'creator': 'alice'
            },
            {
                'name': 'OralHistory1',
                'product_type': 'Heritage',
                'description': 'Luo Oral Storytelling Archive',
                'is_digital': True,
                'creator': 'charlie'
            },
            {
                'name': 'AIModel1',
                'product_type': 'Software',
                'category': 'AI/ML',
                'description': 'AI model for image recognition',
                'is_digital': True,
                'is_license_based': True,
                'creator': 'david'
            },
            {
                'name': 'Game1',
                'product_type': 'Software',
                'category': 'Gaming',
                'description': 'Indie Game built in Unity',
                'is_digital': True,
                'creator': 'david'
            }
        ]
        
        products = {}
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'product_type': product_data['product_type'],
                    'category': product_data.get('category', ''),
                    'description': product_data['description'],
                    'is_physical': product_data.get('is_physical', False),
                    'is_digital': product_data.get('is_digital', False),
                    'is_redeemable': product_data.get('is_redeemable', False),
                    'has_digital_scan': product_data.get('has_digital_scan', False),
                    'is_license_based': product_data.get('is_license_based', False),
                    'creator': creators[product_data['creator']]
                }
            )
            products[product_data['name']] = product
            
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        # Create NFTs
        nfts_data = [
            {
                'token_id': 'NFT_MaasaiNecklace',
                'product': 'Maasai_Necklace',
                'creator': 'alice'
            },
            {
                'token_id': 'NFT_AfrobeatTrack1',
                'product': 'AfrobeatTrack1',
                'creator': 'bob'
            },
            {
                'token_id': 'NFT_Shuka1',
                'product': 'Maasai_Shuka',
                'creator': 'charlie'
            },
            {
                'token_id': 'NFT_Safari1',
                'product': 'Safari_Package1',
                'creator': 'alice'
            },
            {
                'token_id': 'NFT_OralHistory1',
                'product': 'OralHistory1',
                'creator': 'charlie'
            },
            {
                'token_id': 'NFT_AIModel1',
                'product': 'AIModel1',
                'creator': 'david'
            },
            {
                'token_id': 'NFT_Game1',
                'product': 'Game1',
                'creator': 'david'
            }
        ]
        
        nfts = {}
        for nft_data in nfts_data:
            nft, created = NFT.objects.get_or_create(
                token_id=nft_data['token_id'],
                defaults={
                    'product': products[nft_data['product']],
                    'creator': creators[nft_data['creator']]
                }
            )
            nfts[nft_data['token_id']] = nft
            
            if created:
                self.stdout.write(f'Created NFT: {nft.token_id}')
        
        # Create utilities
        utilities_data = [
            {'nft': 'NFT_MaasaiNecklace', 'utility_type': 'provenance'},
            {'nft': 'NFT_MaasaiNecklace', 'utility_type': 'resale_rights'},
            {'nft': 'NFT_AfrobeatTrack1', 'utility_type': 'streaming_rights'},
            {'nft': 'NFT_AfrobeatTrack1', 'utility_type': 'royalties'},
            {'nft': 'NFT_Shuka1', 'utility_type': 'redeem_physical'},
            {'nft': 'NFT_Shuka1', 'utility_type': 'digital_wearable'},
            {'nft': 'NFT_Safari1', 'utility_type': 'redeemable_experience'},
            {'nft': 'NFT_Safari1', 'utility_type': 'eco_tourism_support'},
            {'nft': 'NFT_OralHistory1', 'utility_type': 'archive_access'},
            {'nft': 'NFT_OralHistory1', 'utility_type': 'preservation_funding'},
            {'nft': 'NFT_AIModel1', 'utility_type': 'license_key'},
            {'nft': 'NFT_AIModel1', 'utility_type': 'subscription_access'},
            {'nft': 'NFT_AIModel1', 'utility_type': 'royalty_share'},
            {'nft': 'NFT_Game1', 'utility_type': 'lifetime_access'},
            {'nft': 'NFT_Game1', 'utility_type': 'in_game_assets'},
            {'nft': 'NFT_Game1', 'utility_type': 'updates_access'}
        ]
        
        for utility_data in utilities_data:
            utility, created = Utility.objects.get_or_create(
                nft=nfts[utility_data['nft']],
                utility_type=utility_data['utility_type']
            )
            if created:
                self.stdout.write(f'Created utility: {utility.utility_type} for {utility.nft.token_id}')
        
        # Create ownerships
        ownerships_data = [
            {'nft': 'NFT_MaasaiNecklace', 'creator': 'alice', 'percentage': 70.0},
            {'nft': 'NFT_MaasaiNecklace', 'creator': 'bob', 'percentage': 30.0},
            {'nft': 'NFT_AfrobeatTrack1', 'creator': 'bob', 'percentage': 100.0},
            {'nft': 'NFT_Shuka1', 'creator': 'charlie', 'percentage': 100.0},
            {'nft': 'NFT_Safari1', 'creator': 'alice', 'percentage': 60.0},
            {'nft': 'NFT_Safari1', 'creator': 'bob', 'percentage': 40.0},
            {'nft': 'NFT_OralHistory1', 'creator': 'charlie', 'percentage': 100.0},
            {'nft': 'NFT_AIModel1', 'creator': 'david', 'percentage': 100.0},
            {'nft': 'NFT_Game1', 'creator': 'david', 'percentage': 100.0}
        ]
        
        for ownership_data in ownerships_data:
            ownership, created = Ownership.objects.get_or_create(
                nft=nfts[ownership_data['nft']],
                creator=creators[ownership_data['creator']],
                defaults={'percentage': ownership_data['percentage']}
            )
            if created:
                self.stdout.write(f'Created ownership: {ownership.creator.user.username} owns {ownership.percentage}% of {ownership.nft.token_id}')
        
        # Create dynamic ownership rules
        dynamic_ownerships_data = [
            {
                'nft': 'NFT_MaasaiNecklace',
                'rule_type': 'transfer_rule',
                'rule_description': 'Bob can gain +10% if he contributes 100 sales'
            },
            {
                'nft': 'NFT_AfrobeatTrack1',
                'rule_type': 'decay_rule',
                'rule_description': 'Ownership reduces by 5% if not maintained with updates'
            }
        ]
        
        for rule_data in dynamic_ownerships_data:
            rule, created = DynamicOwnership.objects.get_or_create(
                nft=nfts[rule_data['nft']],
                rule_type=rule_data['rule_type'],
                defaults={'rule_description': rule_data['rule_description']}
            )
            if created:
                self.stdout.write(f'Created dynamic ownership rule: {rule.rule_type} for {rule.nft.token_id}')
        
        # Create governance votes
        governance_votes_data = [
            {'nft': 'NFT_Safari1', 'creator': 'alice', 'weight': 0.6},
            {'nft': 'NFT_Safari1', 'creator': 'bob', 'weight': 0.4}
        ]
        
        for vote_data in governance_votes_data:
            vote, created = GovernanceVote.objects.get_or_create(
                nft=nfts[vote_data['nft']],
                creator=creators[vote_data['creator']],
                defaults={'weight': vote_data['weight']}
            )
            if created:
                self.stdout.write(f'Created governance vote: {vote.creator.user.username} on {vote.nft.token_id}')
        
        # Create utility gates
        utility_gates_data = [
            {'nft': 'NFT_Shuka1', 'utility_type': 'redeem_physical', 'condition': '>=20% ownership required'},
            {'nft': 'NFT_AIModel1', 'utility_type': 'royalty_share', 'condition': '>=50% ownership required'},
            {'nft': 'NFT_Game1', 'utility_type': 'updates_access', 'condition': 'subscription_active'}
        ]
        
        for gate_data in utility_gates_data:
            utility = Utility.objects.get(nft=nfts[gate_data['nft']], utility_type=gate_data['utility_type'])
            gate, created = UtilityGate.objects.get_or_create(
                nft=nfts[gate_data['nft']],
                utility=utility,
                defaults={'condition': gate_data['condition']}
            )
            if created:
                self.stdout.write(f'Created utility gate: {gate.condition} for {gate.utility.utility_type}')
        
        # Create impact scores
        impact_scores_data = [
            {'nft': 'NFT_Safari1', 'heritage_value': 90, 'sustainability_score': 85, 'sdg_alignment': ['Tourism', 'Wildlife_Protection']},
            {'nft': 'NFT_OralHistory1', 'heritage_value': 95, 'sustainability_score': 70, 'sdg_alignment': ['Culture', 'Education']},
            {'nft': 'NFT_AIModel1', 'heritage_value': 40, 'sustainability_score': 60, 'sdg_alignment': ['Innovation', 'Tech4Good']},
            {'nft': 'NFT_MaasaiNecklace', 'heritage_value': 85, 'sustainability_score': 80, 'sdg_alignment': ['Artisan_Economy', 'Women_Empowerment']}
        ]
        
        for score_data in impact_scores_data:
            score, created = ImpactScore.objects.get_or_create(
                nft=nfts[score_data['nft']],
                defaults={
                    'heritage_value': score_data['heritage_value'],
                    'sustainability_score': score_data['sustainability_score'],
                    'sdg_alignment': score_data['sdg_alignment']
                }
            )
            if created:
                self.stdout.write(f'Created impact score for {score.nft.token_id}')
        
        # Create funding thresholds
        funding_thresholds_data = [
            {'nft': 'NFT_MaasaiNecklace', 'amount': 500},
            {'nft': 'NFT_AfrobeatTrack1', 'amount': 1000},
            {'nft': 'NFT_Shuka1', 'amount': 700},
            {'nft': 'NFT_Safari1', 'amount': 2000},
            {'nft': 'NFT_OralHistory1', 'amount': 1500},
            {'nft': 'NFT_AIModel1', 'amount': 5000},
            {'nft': 'NFT_Game1', 'amount': 3000}
        ]
        
        for threshold_data in funding_thresholds_data:
            threshold, created = FundingThreshold.objects.get_or_create(
                nft=nfts[threshold_data['nft']],
                defaults={'amount': threshold_data['amount']}
            )
            if created:
                self.stdout.write(f'Created funding threshold: {threshold.amount} for {threshold.nft.token_id}')
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded marketplace knowledge base data!'))