# Generated manually for marketplace app

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_address', models.CharField(max_length=255, unique=True)),
                ('skills', models.JSONField(default=list)),
                ('reputation_score', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('bio', models.TextField(blank=True)),
                ('profile_image', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='creator_profile', to='auth.user')),
            ],
            options={
                'ordering': ['-reputation_score'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('product_type', models.CharField(choices=[('ArtCraft', 'Art & Craft'), ('Music', 'Music'), ('Fashion', 'Fashion'), ('Tourism', 'Tourism'), ('Heritage', 'Heritage'), ('Software', 'Software')], max_length=20)),
                ('category', models.CharField(blank=True, choices=[('Beadwork', 'Beadwork'), ('Afrobeat', 'Afrobeat'), ('Textile', 'Textile'), ('AI/ML', 'AI/ML'), ('Gaming', 'Gaming'), ('Safari', 'Safari'), ('Oral_History', 'Oral History')], max_length=20)),
                ('description', models.TextField()),
                ('is_physical', models.BooleanField(default=False)),
                ('is_digital', models.BooleanField(default=False)),
                ('is_redeemable', models.BooleanField(default=False)),
                ('has_digital_scan', models.BooleanField(default=False)),
                ('is_license_based', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('tags', models.JSONField(default=list)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='marketplace.creator')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='NFT',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token_id', models.CharField(max_length=255, unique=True)),
                ('blockchain_address', models.CharField(max_length=255)),
                ('contract_address', models.CharField(max_length=255)),
                ('metadata_uri', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nft', to='marketplace.product')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Utility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utility_type', models.CharField(choices=[('provenance', 'Provenance'), ('resale_rights', 'Resale Rights'), ('streaming_rights', 'Streaming Rights'), ('royalties', 'Royalties'), ('redeem_physical', 'Redeem Physical'), ('digital_wearable', 'Digital Wearable'), ('redeemable_experience', 'Redeemable Experience'), ('eco_tourism_support', 'Eco Tourism Support'), ('archive_access', 'Archive Access'), ('preservation_funding', 'Preservation Funding'), ('license_key', 'License Key'), ('subscription_access', 'Subscription Access'), ('royalty_share', 'Royalty Share'), ('lifetime_access', 'Lifetime Access'), ('in_game_assets', 'In-Game Assets'), ('updates_access', 'Updates Access')], max_length=30)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='utilities', to='marketplace.nft')),
            ],
            options={
                'unique_together': {('nft', 'utility_type')},
            },
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('acquired_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to='marketplace.nft')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_nfts', to='marketplace.creator')),
            ],
            options={
                'unique_together': {('nft', 'owner')},
            },
        ),
        migrations.CreateModel(
            name='DynamicOwnership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_type', models.CharField(max_length=50)),
                ('rule_description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_ownership_rules', to='marketplace.nft')),
            ],
        ),
        migrations.CreateModel(
            name='GovernanceVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, default=1.0, max_digits=3)),
                ('is_reputation_weighted', models.BooleanField(default=True)),
                ('vote_data', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='governance_votes', to='marketplace.nft')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes_cast', to='marketplace.creator')),
            ],
            options={
                'unique_together': {('nft', 'voter')},
            },
        ),
        migrations.CreateModel(
            name='UtilityGate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='utility_gates', to='marketplace.nft')),
                ('utility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gates', to='marketplace.utility')),
            ],
        ),
        migrations.CreateModel(
            name='ImpactScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heritage_value', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('sustainability_score', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('sdg_alignment', models.JSONField(default=list)),
                ('calculated_at', models.DateTimeField(auto_now_add=True)),
                ('nft', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='impact_score', to='marketplace.nft')),
            ],
        ),
        migrations.CreateModel(
            name='FundingThreshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('is_met', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('met_at', models.DateTimeField(blank=True, null=True)),
                ('nft', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='funding_threshold', to='marketplace.nft')),
            ],
        ),
        migrations.CreateModel(
            name='NFTHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('minted', 'Minted'), ('sold', 'Sold'), ('transferred', 'Transferred'), ('utility_used', 'Utility Used'), ('governance_vote', 'Governance Vote'), ('ownership_changed', 'Ownership Changed'), ('funding_met', 'Funding Threshold Met')], max_length=20)),
                ('action_data', models.JSONField(default=dict)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='marketplace.nft')),
                ('performed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketplace.creator')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='SmartFunction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('function_type', models.CharField(choices=[('append_history', 'Append History'), ('impact_score', 'Calculate Impact Score'), ('is_creator', 'Check Creator Status'), ('ownership_calculation', 'Ownership Calculation'), ('utility_validation', 'Utility Validation')], max_length=30)),
                ('description', models.TextField()),
                ('parameters', models.JSONField(default=dict)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreatorStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_nfts_created', models.IntegerField(default=0)),
                ('total_sales', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total_royalties_earned', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('average_rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('followers_count', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='marketplace.creator')),
            ],
        ),
        migrations.CreateModel(
            name='MarketplaceConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True)),
                ('value', models.JSONField()),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]