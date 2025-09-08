# Marketplace API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Creators

#### List Creators
```
GET /api/creators/
```
**Query Parameters:**
- `reputation_score`: Filter by reputation score
- `skills`: Filter by skills (comma-separated)
- `search`: Search in username, email, wallet_address, bio
- `ordering`: Order by reputation_score, created_at, updated_at

#### Get Creator Details
```
GET /api/creators/{id}/
```

#### Create Creator
```
POST /api/creators/
```
**Body:**
```json
{
    "user_id": 1,
    "wallet_address": "0x123...",
    "skills": ["art", "beadwork"],
    "reputation_score": 80,
    "bio": "Artist and beadwork specialist",
    "profile_image": "https://example.com/image.jpg"
}
```

#### Update Creator
```
PUT /api/creators/{id}/
PATCH /api/creators/{id}/
```

#### Delete Creator
```
DELETE /api/creators/{id}/
```

#### Creator-specific endpoints
```
GET /api/creators/{id}/nfts/          # Get creator's NFTs
GET /api/creators/{id}/products/      # Get creator's products
GET /api/creators/{id}/ownerships/    # Get creator's ownerships
POST /api/creators/{id}/update_reputation/  # Update reputation score
```

### Products

#### List Products
```
GET /api/products/
```
**Query Parameters:**
- `product_type`: Filter by product type
- `category`: Filter by category
- `is_physical`: Filter physical products
- `is_digital`: Filter digital products
- `creator`: Filter by creator ID
- `search`: Search in name, description
- `ordering`: Order by created_at, updated_at

#### Get Product Details
```
GET /api/products/{id}/
```

#### Create Product
```
POST /api/products/
```
**Body:**
```json
{
    "name": "Maasai Necklace",
    "product_type": "ArtCraft",
    "category": "Beadwork",
    "description": "Original Maasai Bead Necklace",
    "is_physical": true,
    "is_digital": false,
    "is_redeemable": false,
    "has_digital_scan": true,
    "is_license_based": false,
    "creator_id": 1
}
```

#### Product-specific endpoints
```
GET /api/products/{id}/nft/  # Get associated NFT
```

### NFTs

#### List NFTs
```
GET /api/nfts/
```
**Query Parameters:**
- `is_minted`: Filter minted NFTs
- `is_listed`: Filter listed NFTs
- `blockchain`: Filter by blockchain
- `creator`: Filter by creator ID
- `search`: Search in token_id, product name
- `ordering`: Order by created_at, updated_at

#### Get NFT Details
```
GET /api/nfts/{id}/
```

#### Create NFT
```
POST /api/nfts/
```
**Body:**
```json
{
    "token_id": "NFT_001",
    "product": "product_uuid",
    "creator": 1,
    "metadata_uri": "https://ipfs.io/metadata.json",
    "blockchain": "Ethereum",
    "contract_address": "0x123..."
}
```

#### NFT-specific endpoints
```
POST /api/nfts/{id}/mint/              # Mint NFT
POST /api/nfts/{id}/list_for_sale/     # List for sale
POST /api/nfts/{id}/transfer_ownership/ # Transfer ownership
GET /api/nfts/{id}/utilities/          # Get utilities
GET /api/nfts/{id}/ownerships/         # Get ownerships
GET /api/nfts/{id}/history/            # Get transaction history
```

#### Mint NFT
```
POST /api/nfts/{id}/mint/
```
**Body:**
```json
{
    "token_id": "NFT_001",
    "metadata_uri": "https://ipfs.io/metadata.json",
    "blockchain": "Ethereum",
    "contract_address": "0x123..."
}
```

#### Transfer Ownership
```
POST /api/nfts/{id}/transfer_ownership/
```
**Body:**
```json
{
    "from_creator_id": 1,
    "to_creator_id": 2,
    "percentage": 25.5,
    "reason": "Collaboration agreement"
}
```

### Utilities

#### List Utilities
```
GET /api/utilities/
```
**Query Parameters:**
- `utility_type`: Filter by utility type
- `is_active`: Filter active utilities
- `nft`: Filter by NFT ID
- `search`: Search in description

#### Create Utility
```
POST /api/utilities/
```
**Body:**
```json
{
    "nft": "nft_uuid",
    "utility_type": "provenance",
    "description": "Provenance tracking utility",
    "is_active": true
}
```

### Ownership

#### List Ownerships
```
GET /api/ownerships/
```
**Query Parameters:**
- `nft`: Filter by NFT ID
- `creator`: Filter by creator ID
- `is_active`: Filter active ownerships
- `ordering`: Order by percentage, created_at

#### Create Ownership
```
POST /api/ownerships/
```
**Body:**
```json
{
    "nft": "nft_uuid",
    "creator_id": 1,
    "percentage": 100.0,
    "is_active": true
}
```

### Dynamic Ownership

#### List Dynamic Ownership Rules
```
GET /api/dynamic-ownerships/
```
**Query Parameters:**
- `nft`: Filter by NFT ID
- `rule_type`: Filter by rule type
- `is_active`: Filter active rules
- `search`: Search in rule description

#### Create Dynamic Ownership Rule
```
POST /api/dynamic-ownerships/
```
**Body:**
```json
{
    "nft": "nft_uuid",
    "rule_type": "transfer_rule",
    "rule_description": "Bob can gain +10% if he contributes 100 sales",
    "is_active": true
}
```

### Governance Votes

#### List Governance Votes
```
GET /api/governance-votes/
```
**Query Parameters:**
- `nft`: Filter by NFT ID
- `creator`: Filter by creator ID
- `is_reputation_weighted`: Filter reputation-weighted votes
- `ordering`: Order by weight, vote_timestamp

#### Create Governance Vote
```
POST /api/governance-votes/
```
**Body:**
```json
{
    "nft": "nft_uuid",
    "creator_id": 1,
    "weight": 0.6,
    "is_reputation_weighted": true
}
```

### Utility Gates

#### List Utility Gates
```
GET /api/utility-gates/
```
**Query Parameters:**
- `nft`: Filter by NFT ID
- `utility`: Filter by utility ID
- `is_active`: Filter active gates
- `search`: Search in condition

#### Create Utility Gate
```
POST /api/utility-gates/
```
**Body:**
```json
{
    "nft": "nft_uuid",
    "utility_id": 1,
    "condition": ">=20% ownership required",
    "is_active": true
}
```

### Impact Scores

#### List Impact Scores
```
GET /api/impact-scores/
```
**Query Parameters:**
- `nft`: Filter by NFT ID
- `ordering`: Order by heritage_value, sustainability_score, calculated_at

#### Create Impact Score
```
POST /api/impact-scores/
```
**Body:**
```json
{
    "nft": "nft_uuid",
    "heritage_value": 85,
    "sustainability_score": 80,
    "sdg_alignment": ["Artisan_Economy", "Women_Empowerment"]
}
```

#### Recalculate Impact Score
```
POST /api/impact-scores/{id}/recalculate/
```
**Body:**
```json
{
    "heritage_value": 90,
    "sustainability_score": 85,
    "sdg_alignment": ["Tourism", "Wildlife_Protection"]
}
```

### Funding Thresholds

#### List Funding Thresholds
```
GET /api/funding-thresholds/
```
**Query Parameters:**
- `nft`: Filter by NFT ID
- `currency`: Filter by currency
- `is_active`: Filter active thresholds
- `ordering`: Order by amount, created_at

#### Create Funding Threshold
```
POST /api/funding-thresholds/
```
**Body:**
```json
{
    "nft": "nft_uuid",
    "amount": 1000.00,
    "currency": "USD",
    "is_active": true
}
```

### NFT History

#### List NFT History
```
GET /api/nft-history/
```
**Query Parameters:**
- `nft`: Filter by NFT ID
- `action_type`: Filter by action type
- `user`: Filter by user ID
- `ordering`: Order by timestamp

### Marketplace Statistics

#### Get Current Stats
```
GET /api/marketplace-stats/current/
```

#### Get Analytics
```
GET /api/marketplace-stats/analytics/
```

## Example API Usage

### Creating a Complete NFT Workflow

1. **Create Creator**
```bash
curl -X POST http://localhost:8000/api/creators/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "wallet_address": "0x1234567890abcdef",
    "skills": ["art", "beadwork"],
    "reputation_score": 85
  }'
```

2. **Create Product**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maasai Necklace",
    "product_type": "ArtCraft",
    "category": "Beadwork",
    "description": "Original Maasai Bead Necklace",
    "is_physical": true,
    "has_digital_scan": true,
    "creator_id": 1
  }'
```

3. **Create NFT**
```bash
curl -X POST http://localhost:8000/api/nfts/ \
  -H "Content-Type: application/json" \
  -d '{
    "token_id": "NFT_MaasaiNecklace",
    "product": "product_uuid",
    "creator": 1
  }'
```

4. **Add Utilities**
```bash
curl -X POST http://localhost:8000/api/utilities/ \
  -H "Content-Type: application/json" \
  -d '{
    "nft": "nft_uuid",
    "utility_type": "provenance",
    "description": "Provenance tracking"
  }'
```

5. **Set Ownership**
```bash
curl -X POST http://localhost:8000/api/ownerships/ \
  -H "Content-Type: application/json" \
  -d '{
    "nft": "nft_uuid",
    "creator_id": 1,
    "percentage": 100.0
  }'
```

6. **Mint NFT**
```bash
curl -X POST http://localhost:8000/api/nfts/{nft_id}/mint/ \
  -H "Content-Type: application/json" \
  -d '{
    "token_id": "NFT_MaasaiNecklace",
    "blockchain": "Ethereum"
  }'
```

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200 OK`: Success
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error response format:
```json
{
    "error": "Error message",
    "detail": "Detailed error information"
}
```

## Pagination

List endpoints support pagination with the following query parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

Response format:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/nfts/?page=2",
    "previous": null,
    "results": [...]
}
```