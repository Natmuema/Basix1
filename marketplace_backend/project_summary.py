#!/usr/bin/env python3
"""
Project summary script to display the marketplace backend structure
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from django.db import models
from creators.models import Creator
from products.models import Product
from nfts.models import NFT, Ownership, Utility
from utilities.models import Transaction

print("=== Marketplace Backend Summary ===\n")

print("📊 Database Status:")
print(f"  • Creators: {Creator.objects.count()}")
print(f"  • Products: {Product.objects.count()}")
print(f"  • NFTs: {NFT.objects.count()}")
print(f"  • Ownerships: {Ownership.objects.count()}")
print(f"  • Utilities: {Utility.objects.count()}")
print(f"  • Transactions: {Transaction.objects.count()}")

print("\n🎨 Product Types:")
products_by_type = {}
for product in Product.objects.all():
    if product.product_type not in products_by_type:
        products_by_type[product.product_type] = 0
    products_by_type[product.product_type] += 1

for ptype, count in products_by_type.items():
    print(f"  • {ptype}: {count}")

print("\n💎 NFT Funding Status:")
funded = NFT.objects.filter(current_funding__gte=models.F('funding_threshold')).count()
print(f"  • Funded: {funded}")
print(f"  • Not Funded: {NFT.objects.count() - funded}")

print("\n👥 Top Creators by Reputation:")
top_creators = Creator.objects.order_by('-reputation_score')[:3]
for creator in top_creators:
    username = creator.user.username if creator.user else "Anonymous"
    print(f"  • {username}: {creator.reputation_score} reputation")

print("\n🌟 High Impact NFTs:")
high_impact_nfts = NFT.objects.filter(
    heritage_value__gte=80,
    sustainability_score__gte=80
)[:3]
for nft in high_impact_nfts:
    print(f"  • {nft.name}: Heritage {nft.heritage_value}, Sustainability {nft.sustainability_score}")

print("\n✅ Project Setup Complete!")
print("\nTo run the server: python3 manage.py runserver")
print("Admin panel: http://localhost:8000/admin/ (admin/admin123)")
print("API Root: http://localhost:8000/api/")