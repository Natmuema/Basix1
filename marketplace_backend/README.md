# Marketplace Backend

A Django REST API backend for a decentralized marketplace that supports creators, products, NFTs with utilities, fractional ownership, and impact scoring.

## Features

- **Creator Management**: User profiles with wallet addresses, skills, and reputation scores
- **Product Catalog**: Support for physical, digital, and redeemable products across multiple categories
- **NFT System**: NFTs linked to products with funding thresholds and impact metrics
- **Utilities**: Various utility types attached to NFTs with ownership-based gating
- **Fractional Ownership**: Support for multiple owners per NFT with dynamic ownership rules
- **Governance**: Reputation-weighted voting system for NFT holders
- **Impact Scoring**: Heritage value and sustainability metrics for each NFT
- **Transaction History**: Complete transaction tracking with blockchain integration support
- **Analytics**: Marketplace statistics and impact metrics tracking

## Technology Stack

- Django 5.2.5
- Django REST Framework 3.16.1
- SQLite (default, can be changed to PostgreSQL)
- CORS support for frontend integration

## Installation

1. Clone the repository:
```bash
cd /workspace/marketplace_backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

4. Create a superuser:
```bash
python3 manage.py createsuperuser
```

5. Run the development server:
```bash
python3 manage.py runserver
```

## API Endpoints

### Creators
- `GET /api/creators/` - List all creators
- `POST /api/creators/` - Create a new creator
- `GET /api/creators/{id}/` - Get creator details
- `PUT /api/creators/{id}/` - Update creator
- `DELETE /api/creators/{id}/` - Delete creator
- `GET /api/creators/{id}/nfts/` - Get NFTs owned by creator
- `GET /api/creators/{id}/created_nfts/` - Get NFTs created by creator
- `POST /api/creators/{id}/update_reputation/` - Update creator reputation
- `GET /api/creators/top_creators/` - Get top creators by reputation
- `GET /api/creators/verified/` - Get verified creators

### Products
- `GET /api/products/` - List all products (with filtering)
- `POST /api/products/` - Create a new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product
- `GET /api/products/{id}/nfts/` - Get NFTs linked to product
- `GET /api/products/statistics/` - Get product statistics
- `GET /api/products/cultural_heritage/` - Get cultural heritage products
- `GET /api/products/software_products/` - Get software products

### NFTs
- `GET /api/nfts/` - List all NFTs (with filtering)
- `POST /api/nfts/` - Create a new NFT
- `GET /api/nfts/{id}/` - Get NFT details
- `PUT /api/nfts/{id}/` - Update NFT
- `DELETE /api/nfts/{id}/` - Delete NFT
- `POST /api/nfts/{id}/append_history/` - Append to NFT history
- `GET /api/nfts/{id}/ownership_distribution/` - Get ownership distribution
- `POST /api/nfts/{id}/add_ownership/` - Add/update ownership
- `POST /api/nfts/{id}/add_utility/` - Add utility to NFT
- `GET /api/nfts/{id}/accessible_utilities/` - Get accessible utilities for creator
- `POST /api/nfts/{id}/add_governance_vote/` - Add governance vote
- `POST /api/nfts/{id}/contribute_funding/` - Contribute funding
- `POST /api/nfts/{id}/record_metrics/` - Record impact metrics
- `GET /api/nfts/top_funded/` - Get top funded NFTs
- `GET /api/nfts/high_impact/` - Get high impact NFTs

### Transactions
- `GET /api/transactions/` - List transactions (with filtering)
- `POST /api/transactions/` - Create transaction
- `GET /api/transactions/{id}/` - Get transaction details

### Impact Metrics
- `GET /api/impact-metrics/` - List impact metrics
- `GET /api/impact-metrics/{id}/` - Get metric details
- `GET /api/impact-metrics/latest_by_nft/` - Get latest metrics by NFT

### Marketplace Stats
- `GET /api/marketplace-stats/` - List marketplace statistics
- `GET /api/marketplace-stats/current/` - Get current day stats
- `POST /api/marketplace-stats/generate/` - Generate stats for date

### Utilities
- `POST /api/impact-score/` - Calculate NFT impact score
- `GET /api/utility-access/` - Check utility access for creator

## Data Models

### Creator
- User profile with wallet address
- Skills array
- Reputation score (0-100)
- Profile image support

### Product
- Multiple types: ArtCraft, Music, Fashion, Tourism, Heritage, Software
- Properties: physical, digital, redeemable, license-based
- Media file support

### NFT
- Linked to products
- Funding threshold and current funding tracking
- Heritage value and sustainability scores
- SDG alignment
- Transaction history

### Ownership
- Fractional ownership support
- Dynamic ownership rules (transfer and decay)
- Percentage-based (0-100%)

### Utility
- 16 different utility types
- Ownership-based gating
- Conditional access rules

### GovernanceVote
- Reputation-weighted voting
- Effective weight calculation

## Admin Interface

Access the Django admin at `/admin/` with your superuser credentials to manage all data models.

## Development

### Running Tests
```bash
python3 manage.py test
```

### Making Migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Loading Sample Data
Create a Django management command or use the admin interface to populate sample data based on the knowledge base.

## Environment Variables

Create a `.env` file in the project root:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

## CORS Configuration

Currently configured to allow:
- http://localhost:3000
- http://localhost:8000

Update in `settings.py` for production.

## Media Files

Uploaded files are stored in the `media/` directory. Ensure proper permissions and configure cloud storage for production.

## Next Steps

1. Add authentication (JWT tokens)
2. Implement blockchain integration
3. Add WebSocket support for real-time updates
4. Set up celery for background tasks
5. Add comprehensive API documentation (Swagger/ReDoc)
6. Implement caching with Redis
7. Add comprehensive test coverage
8. Set up CI/CD pipeline