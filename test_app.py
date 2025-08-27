#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/workspace/backend/marketplace_project')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace_project.settings')
django.setup()

# Test imports
try:
    from marketplace.models import Creator, Product, NFT
    print("✅ Successfully imported marketplace models")
    
    # Test creating a simple object
    from django.contrib.auth.models import User
    
    # Create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("✅ Created test user")
    
    # Test creating a creator
    creator, created = Creator.objects.get_or_create(
        user=user,
        defaults={
            'wallet_address': 'test_wallet_123',
            'skills': ['test_skill'],
            'reputation_score': 50
        }
    )
    if created:
        print("✅ Created test creator")
    
    print("✅ All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()