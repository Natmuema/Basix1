# Marketplace Backend

A comprehensive Django REST API backend for a cultural and creative marketplace that supports NFTs, creators, products, and various utility types.

## Features

### Core Entities
- **Creators**: Artists, developers, and content creators with reputation scoring
- **Products**: Various product types (Art & Craft, Music, Fashion, Tourism, Heritage, Software)
- **NFTs**: Digital tokens linked to products with blockchain support
- **Utilities**: NFT utilities like provenance, streaming rights, royalties, etc.
- **Ownership**: Fractional ownership with dynamic rules
- **Governance**: Reputation-weighted voting system
- **Impact Scoring**: Heritage value and sustainability scoring
- **Funding Thresholds**: Funding goals for projects

### Advanced Features
- **Dynamic Ownership**: Rules for ownership changes based on conditions
- **Utility Gating**: Conditional access to NFT utilities
- **Governance Voting**: Weighted voting system for NFT decisions
- **Impact Assessment**: SDG alignment and sustainability scoring
- **Transaction History**: Complete audit trail for all NFT actions
- **Marketplace Analytics**: Comprehensive statistics and insights

## Technology Stack

- **Django 5.2.5**: Web framework
- **Django REST Framework 3.14.0**: API framework
- **Django CORS Headers**: Cross-origin resource sharing
- **Django Filter**: Advanced filtering capabilities
- **SQLite**: Database (can be easily migrated to PostgreSQL/MySQL)

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd backend
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
cd basix
python manage.py migrate
```

5. **Load sample data**
```bash
python manage.py load_knowledge_base
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver 0.0.0.0:8000
```

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### Authentication
Currently configured for public access. JWT authentication can be enabled by updating settings.

### Main Endpoints

#### Creators
- `GET /api/creators/` - List all creators
- `GET /api/creators/{id}/` - Get creator details
- `POST /api/creators/` - Create new creator
- `PUT /api/creators/{id}/` - Update creator
- `DELETE /api/creators/{id}/` - Delete creator

#### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `POST /api/products/` - Create new product
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

#### NFTs
- `GET /api/nfts/` - List all NFTs
- `GET /api/nfts/{id}/` - Get NFT details
- `POST /api/nfts/` - Create new NFT
- `POST /api/nfts/{id}/mint/` - Mint NFT
- `POST /api/nfts/{id}/list_for_sale/` - List NFT for sale
- `POST /api/nfts/{id}/transfer_ownership/` - Transfer ownership

#### Utilities
- `GET /api/utilities/` - List all utilities
- `POST /api/utilities/` - Create new utility

#### Ownership
- `GET /api/ownerships/` - List all ownerships
- `POST /api/ownerships/` - Create new ownership

#### Impact Scores
- `GET /api/impact-scores/` - List all impact scores
- `POST /api/impact-scores/` - Create new impact score
- `POST /api/impact-scores/{id}/recalculate/` - Recalculate impact score

#### Marketplace Statistics
- `GET /api/marketplace-stats/current/` - Get current stats
- `GET /api/marketplace-stats/analytics/` - Get detailed analytics

## Data Models

### Creator
```python
{
    "id": 1,
    "user": {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
        "first_name": "Alice",
        "last_name": "Creator"
    },
    "wallet_address": "addr1",
    "skills": ["art", "beadwork"],
    "reputation_score": 80,
    "bio": "Artist and beadwork specialist",
    "profile_image": "https://example.com/image.jpg"
}
```

### Product
```python
{
    "id": "uuid",
    "name": "Maasai Necklace",
    "product_type": "ArtCraft",
    "category": "Beadwork",
    "description": "Original Maasai Bead Necklace",
    "is_physical": true,
    "is_digital": false,
    "is_redeemable": false,
    "has_digital_scan": true,
    "is_license_based": false,
    "creator": 1
}
```

### NFT
```python
{
    "id": "uuid",
    "token_id": "NFT_MaasaiNecklace",
    "product": "product_uuid",
    "creator": 1,
    "metadata_uri": "https://ipfs.io/metadata.json",
    "blockchain": "Ethereum",
    "contract_address": "0x123...",
    "is_minted": false,
    "is_listed": false,
    "utilities": [...],
    "ownerships": [...]
}
```

## Sample Data

The system comes pre-loaded with sample data including:

### Creators
- **Alice** (Reputation: 80) - Art & Beadwork specialist
- **Bob** (Reputation: 70) - Music & Performance artist
- **Charlie** (Reputation: 65) - Fashion & Design creator
- **David** (Reputation: 90) - Software, AI & Games developer

### Products & NFTs
- **Maasai Necklace** (ArtCraft) - Physical beadwork with digital scan
- **Afrobeat Track** (Music) - Digital music with streaming rights
- **Maasai Shuka** (Fashion) - Physical textile with digital wearable
- **Safari Package** (Tourism) - Redeemable experience
- **Oral History** (Heritage) - Digital archive
- **AI Model** (Software) - License-based AI model
- **Indie Game** (Software) - Digital game with lifetime access

### Utilities
- **Provenance** - Track origin and history
- **Streaming Rights** - Music streaming permissions
- **Royalties** - Revenue sharing
- **Redeem Physical** - Physical item redemption
- **Digital Wearable** - Virtual fashion items
- **Archive Access** - Digital content access
- **License Key** - Software licensing
- **Lifetime Access** - Permanent access rights

## Frontend Integration

The backend is designed to work seamlessly with React frontends. See `FRONTEND_INTEGRATION.md` for detailed integration examples.

### API Service Example
```javascript
const API_BASE_URL = 'http://localhost:8000/api';

// Get all creators
const creators = await fetch(`${API_BASE_URL}/creators/`).then(r => r.json());

// Get specific NFT
const nft = await fetch(`${API_BASE_URL}/nfts/${nftId}/`).then(r => r.json());

// Mint an NFT
const minted = await fetch(`${API_BASE_URL}/nfts/${nftId}/mint/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ blockchain: 'Ethereum' })
}).then(r => r.json());
```

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to manage all data through a web interface.

Default superuser credentials:
- Username: `admin`
- Email: `admin@example.com`
- Password: (set during creation)

## Configuration

### Environment Variables
Create a `.env` file in the `basix` directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Database Configuration
The default configuration uses SQLite. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'marketplace_db',
        'USER': 'marketplace_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Development

### Running Tests
```bash
python manage.py test marketplace
```

### Creating Migrations
```bash
python manage.py makemigrations marketplace
```

### Applying Migrations
```bash
python manage.py migrate
```

### Shell Access
```bash
python manage.py shell
```

### Custom Management Commands
```bash
# Load sample data
python manage.py load_knowledge_base

# Create additional sample data
python manage.py create_sample_data
```

## API Documentation

For detailed API documentation, see `API_DOCUMENTATION.md`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.

## Roadmap

- [ ] JWT Authentication
- [ ] WebSocket support for real-time updates
- [ ] File upload support
- [ ] Advanced analytics dashboard
- [ ] Blockchain integration
- [ ] Payment processing
- [ ] Email notifications
- [ ] Mobile API support