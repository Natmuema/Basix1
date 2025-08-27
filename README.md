# Marketplace Knowledge Base - Django Backend

A comprehensive Django REST API backend for a marketplace knowledge base that supports cultural and creative products, NFTs, fractional ownership, governance, and impact scoring.

## Features

### Core Models
- **Creators**: Artists, developers, and content creators with reputation scoring
- **Products**: Various types of creative and cultural products (Art, Music, Fashion, Tourism, Heritage, Software)
- **NFTs**: Blockchain-based digital assets with utilities and ownership
- **Utilities**: Various utilities associated with NFTs (provenance, royalties, streaming rights, etc.)
- **Ownership**: Fractional ownership system with dynamic rules
- **Governance**: Reputation-weighted voting system
- **Impact Scoring**: Heritage value and sustainability scoring with SDG alignment
- **Funding Thresholds**: Crowdfunding and funding milestone tracking

### Advanced Features
- **Dynamic Ownership**: Rules for ownership changes based on conditions
- **Utility Gating**: Conditional access to NFT utilities
- **Smart Functions**: Automated operations and calculations
- **History Tracking**: Complete audit trail of all NFT actions
- **Creator Statistics**: Comprehensive analytics for creators
- **Marketplace Configuration**: Flexible configuration system

## Technology Stack

- **Django 5.2.5**: Web framework
- **Django REST Framework 3.16.1**: API framework
- **Django CORS Headers**: Cross-origin resource sharing
- **Django REST Framework Simple JWT**: JWT authentication
- **Django Filter**: Advanced filtering capabilities
- **SQLite**: Database (can be easily switched to PostgreSQL)

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip

### 1. Clone the Repository
```bash
git clone <repository-url>
cd marketplace_project
```

### 2. Create Virtual Environment
```bash
python3 -m venv marketplace_env
source marketplace_env/bin/activate  # On Windows: marketplace_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Populate Sample Data
```bash
python manage.py populate_marketplace
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

### Creators
- `GET /api/creators/` - List all creators
- `GET /api/creators/{id}/` - Get creator details
- `GET /api/creators/{id}/stats/` - Get creator statistics
- `GET /api/creators/{id}/products/` - Get creator's products
- `GET /api/creators/{id}/owned_nfts/` - Get creator's owned NFTs
- `GET /api/creators/top_creators/` - Get top creators by reputation

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/{id}/nft/` - Get associated NFT
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

### NFTs
- `GET /api/nfts/` - List all NFTs
- `POST /api/nfts/` - Create new NFT
- `GET /api/nfts/{id}/` - Get NFT details
- `POST /api/nfts/{id}/append_history/` - Append action to history
- `POST /api/nfts/{id}/calculate_impact_score/` - Calculate impact score
- `POST /api/nfts/{id}/transfer_ownership/` - Transfer ownership
- `GET /api/nfts/{id}/is_creator/` - Check if user is creator

### Utilities
- `GET /api/utilities/` - List all utilities
- `POST /api/utilities/` - Create new utility
- `GET /api/utilities/{id}/` - Get utility details

### Ownership
- `GET /api/ownerships/` - List all ownership records
- `POST /api/ownerships/` - Create ownership record
- `GET /api/ownerships/{id}/` - Get ownership details

### Governance
- `GET /api/governance-votes/` - List all governance votes
- `POST /api/governance-votes/` - Create governance vote
- `GET /api/governance-votes/{id}/` - Get vote details

### Impact Scores
- `GET /api/impact-scores/` - List all impact scores
- `POST /api/impact-scores/` - Create impact score
- `GET /api/impact-scores/top_impact/` - Get top impact scores

### Funding Thresholds
- `GET /api/funding-thresholds/` - List all funding thresholds
- `POST /api/funding-thresholds/{id}/check_threshold/` - Check if threshold is met

### Marketplace Statistics
- `GET /api/stats/overview/` - Get marketplace overview
- `GET /api/stats/product_types_distribution/` - Get product type distribution
- `GET /api/stats/utility_types_distribution/` - Get utility type distribution

### Configuration
- `GET /api/marketplace-configs/get_config/` - Get marketplace configuration

## Sample Data

The system comes with sample data representing the marketplace knowledge base:

### Creators
- **Alice** (Art & Beadwork, Reputation: 80)
- **Bob** (Music & Performance, Reputation: 70)
- **Charlie** (Fashion & Design, Reputation: 65)
- **David** (Software, AI & Games, Reputation: 90)

### Products & NFTs
1. **Maasai Necklace** (ArtCraft) - Alice
2. **Afrobeat Track 1** (Music) - Bob
3. **Maasai Shuka** (Fashion) - Charlie
4. **Safari Package 1** (Tourism) - Alice & Bob (60/40 ownership)
5. **Oral History 1** (Heritage) - Charlie
6. **AI Model 1** (Software) - David
7. **Game 1** (Software) - David

### Utilities
- Provenance tracking
- Resale rights
- Streaming rights
- Royalties
- Physical redemption
- Digital wearables
- Experience redemption
- Eco-tourism support
- Archive access
- Preservation funding
- License keys
- Subscription access
- Lifetime access
- In-game assets
- Updates access

## Admin Interface

Access the Django admin interface at `/admin/` to manage:
- All models with comprehensive filtering and search
- Creator profiles and statistics
- Products and NFTs
- Ownership and governance records
- Impact scores and funding thresholds
- Marketplace configurations

## API Usage Examples

### Creating a New NFT
```bash
curl -X POST http://localhost:8000/api/nfts/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "token_id": "NFT_MyArtwork",
    "blockchain_address": "0x1234567890abcdef",
    "contract_address": "0xcontract123456",
    "product_data": {
      "name": "My Artwork",
      "product_type": "ArtCraft",
      "category": "Beadwork",
      "description": "Beautiful handmade artwork",
      "is_physical": true,
      "creator_id": 1
    },
    "utilities": ["provenance", "resale_rights"],
    "initial_ownership": 100.00
  }'
```

### Transferring Ownership
```bash
curl -X POST http://localhost:8000/api/nfts/1/transfer_ownership/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "from_owner_id": 1,
    "to_owner_id": 2,
    "nft_id": 1,
    "percentage": 25.00
  }'
```

### Calculating Impact Score
```bash
curl -X POST http://localhost:8000/api/nfts/1/calculate_impact_score/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nft_id": 1,
    "heritage_value": 85,
    "sustainability_score": 80,
    "sdg_alignment": ["Artisan_Economy", "Women_Empowerment"]
  }'
```

## Configuration

The system can be configured through the `MARKETPLACE_SETTINGS` in `settings.py`:

```python
MARKETPLACE_SETTINGS = {
    'DEFAULT_CURRENCY': 'USD',
    'SUPPORTED_CURRENCIES': ['USD', 'EUR', 'GBP', 'KES'],
    'MAX_OWNERSHIP_PERCENTAGE': 100.00,
    'MIN_REPUTATION_SCORE': 0,
    'MAX_REPUTATION_SCORE': 100,
    'DEFAULT_PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 100,
}
```

## Development

### Running Tests
```bash
python manage.py test marketplace
```

### Code Style
The project follows PEP 8 style guidelines. Use a linter like `flake8` or `black` for code formatting.

### Database Migrations
When making model changes:
```bash
python manage.py makemigrations marketplace
python manage.py migrate
```

## Deployment

### Production Settings
For production deployment:
1. Set `DEBUG = False`
2. Configure a production database (PostgreSQL recommended)
3. Set up proper CORS settings
4. Configure static file serving
5. Set up HTTPS
6. Use environment variables for sensitive settings

### Environment Variables
Create a `.env` file for sensitive configuration:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=yourdomain.com
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository or contact the development team.