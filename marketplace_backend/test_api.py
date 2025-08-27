#!/usr/bin/env python3
"""
Simple script to test API endpoints
Run the Django server first: python3 manage.py runserver
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    print("Testing Marketplace API Endpoints...\n")
    
    # Test root endpoint
    print("1. Testing API root:")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # Test creators endpoint
    print("2. Testing creators endpoint:")
    response = requests.get(f"{BASE_URL}/creators/")
    print(f"Status: {response.status_code}")
    print(f"Found {len(response.json()['results'])} creators\n")
    
    # Test products endpoint
    print("3. Testing products endpoint:")
    response = requests.get(f"{BASE_URL}/products/")
    print(f"Status: {response.status_code}")
    print(f"Found {len(response.json()['results'])} products\n")
    
    # Test NFTs endpoint
    print("4. Testing NFTs endpoint:")
    response = requests.get(f"{BASE_URL}/nfts/")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data['results'])} NFTs")
    if data['results']:
        nft = data['results'][0]
        print(f"First NFT: {nft['name']} (Token: {nft['token_id']})")
        print(f"Funding: ${nft['current_funding']} / ${nft['funding_threshold']}")
        print(f"Impact Score: {nft['impact_score']}\n")
    
    # Test product statistics
    print("5. Testing product statistics:")
    response = requests.get(f"{BASE_URL}/products/statistics/")
    print(f"Status: {response.status_code}")
    stats = response.json()
    print(f"Total products: {stats['total_products']}")
    print(f"Physical products: {stats['physical_products']}")
    print(f"Digital products: {stats['digital_products']}")
    print(f"By type: {json.dumps(stats['by_type'], indent=2)}\n")
    
    # Test top creators
    print("6. Testing top creators:")
    response = requests.get(f"{BASE_URL}/creators/top_creators/?limit=3")
    print(f"Status: {response.status_code}")
    creators = response.json()
    for creator in creators:
        print(f"- {creator['wallet_address']}: Reputation {creator['reputation_score']}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_endpoints()